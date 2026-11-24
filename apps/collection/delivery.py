from datetime import timedelta
from smtplib import SMTPRecipientsRefused, SMTPDataError, SMTPSenderRefused, SMTPAuthenticationError
from uuid import UUID

from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Account
from apps.statements.email import StatementEmailSender
from .email import CollectionReminderEmailSender
from .models import CollectionFollowUp, CollectionReminder, DeliveryAttempt

Status = DeliveryAttempt.Status


@transaction.atomic
def reserve(account_id, token, follow_up_id, message, expected_balance, base_url):
    try:
        key = UUID(str(token))
    except ValueError:
        raise ValidationError("Vuelve a abrir el formulario para confirmar el envío.")

    account = Account.objects.select_for_update().get(pk=account_id)
    attempts = account.delivery_attempts.filter(follow_up_id=follow_up_id)
    previous = attempts.filter(pk=key).first()
    if not previous and DeliveryAttempt.objects.filter(pk=key).exists():
        raise ValidationError("Este intento corresponde a otro envío.")
    if previous and previous.status not in (Status.REJECTED, Status.PENDING):
        return previous
    unresolved = attempts.filter(status__in=[Status.PENDING, Status.SENDING, Status.UNKNOWN]).exclude(pk=key).first()
    if unresolved:
        raise ValidationError("Existe un envío pendiente de confirmación. Consulta el historial.")
    balance = account.balance
    recipient = account.customer.email
    if balance <= 0 or not recipient:
        raise ValidationError("Revisa el saldo pendiente y el email del cliente.")
    if follow_up_id:
        follow_up = CollectionFollowUp.objects.select_for_update().get(pk=follow_up_id, account=account)
        if follow_up.status != CollectionFollowUp.Status.ACTIVE or balance != expected_balance:
            raise ValidationError("El seguimiento ha cambiado. Revisa los datos antes de enviar.")
        email = CollectionReminderEmailSender(follow_up).build(message)
    else:
        if account.active_collection_follow_up:
            raise ValidationError("Ya existe un seguimiento activo.")
        email = StatementEmailSender(account).build(base_url)
    if previous and previous.status == Status.PENDING:
        if previous.balance != balance or previous.recipient != recipient or (follow_up_id and previous.body != message):
            raise ValidationError("El intento pendiente corresponde a otros datos.")
        return previous
    fields = dict(account=account, follow_up_id=follow_up_id, recipient=recipient,
                  balance=balance, subject=email.subject, body=email.body, status=Status.PENDING,
                  html=email.alternatives[0].content if email.alternatives else "",
                  pdf=email.attachments[0].content if email.attachments else None)
    if previous:
        attempts.filter(pk=key).update(**fields)
        previous.refresh_from_db()
        return previous
    return DeliveryAttempt.objects.create(pk=key, **fields)


def deliver(account_id, token, *, follow_up_id=None, message="", expected_balance=None, base_url=None):
    attempt = reserve(account_id, token, follow_up_id, message, expected_balance, base_url)
    rows = DeliveryAttempt.objects.filter(pk=attempt.pk)
    if not rows.filter(status=Status.PENDING).update(status=Status.SENDING):
        return rows.values_list("status", flat=True).get()

    email = EmailMultiAlternatives(attempt.subject, attempt.body, to=[attempt.recipient])
    if attempt.html:
        email.attach_alternative(attempt.html, "text/html")
    if attempt.pdf:
        email.attach(f"estado_cuenta_{account_id}.pdf", bytes(attempt.pdf), "application/pdf")
    try:
        status = Status.SENT if email.send() == 1 else Status.REJECTED
    except (SMTPRecipientsRefused, SMTPDataError, SMTPSenderRefused, SMTPAuthenticationError):
        status = Status.REJECTED
    except Exception:
        status = Status.UNKNOWN

    with transaction.atomic():
        if status == Status.SENT:
            account = Account.objects.select_for_update().get(pk=account_id)
            now = timezone.now()
            if follow_up_id:
                CollectionReminder.objects.create(
                    follow_up_id=follow_up_id, recipient_email=attempt.recipient,
                    subject=attempt.subject, message=attempt.body, balance_at_send=attempt.balance,
                )
            else:
                CollectionFollowUp.objects.create(
                    account=account, amount=attempt.balance, sent_at=now,
                    status=CollectionFollowUp.Status.ACTIVE if account.balance > 0 else CollectionFollowUp.Status.COMPLETED,
                    due_date=now.date() + timedelta(days=settings.COLLECTION_PAYMENT_TERM_DAYS),
                )
        rows.update(status=status)
    return status



def report_delivery(request, status):
    if status == Status.SENT:
        messages.success(request, "Envío confirmado por el servidor de correo.")
    elif status == Status.REJECTED:
        messages.error(request, "El servidor ha rechazado el envío. Puedes reintentarlo.")
    else:
        messages.warning(request, "Envío sin confirmar. Comprueba el correo antes de volver a enviarlo.")
