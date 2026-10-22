from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError

from .email import CollectionReminderEmailSender
from .models import CollectionFollowUp, CollectionReminder 
from .integrations import CollectionReminderService

class CollectionFollowUpCancelView(LoginRequiredMixin, View):

    def post(self, request, pk):

        follow_up = get_object_or_404(
            CollectionFollowUp,
            pk=pk,
        )

        if follow_up.status != CollectionFollowUp.Status.ACTIVE:
            messages.error(
                request,
                "Este seguimiento ya no está activo."
            )

            return redirect(
                "accounts:account_detail",
                pk=follow_up.account.pk,
            )

        follow_up.status = CollectionFollowUp.Status.CANCELED
        follow_up.save(update_fields=["status"])

        messages.success(
            request,
            "El seguimiento de cobro se ha cancelado correctamente."
        )

        return redirect(
            "accounts:account_detail",
            pk=follow_up.account.pk,
        )

class CollectionReminderPrepareView(LoginRequiredMixin, View):

    def post(self, request, pk):
        follow_up = get_object_or_404(
            CollectionFollowUp,
            pk=pk,
            status=CollectionFollowUp.Status.ACTIVE,
        )

        try:
            reminder =CollectionReminderService.prepare(follow_up)
        except Exception:
            messages.error(
                request,
                "No se ha podido conectar con el servicio de recordatorios."
            )
            return redirect("dashboard:dashboard")

        return render(
            request,
            "collection/reminder_review.html",
            {
                "follow_up": follow_up,
                "reminder": reminder,
                "original_balance": str(follow_up.account.balance),
            },
        )


class CollectionReminderSendView(LoginRequiredMixin, View):

    def post(self, request, pk):
        follow_up = get_object_or_404(
            CollectionFollowUp.objects.select_related(
                "account__customer",
                "account__season",
            ),
            pk=pk,
        )

        account = follow_up.account
        customer = account.customer

        reminder = request.POST.get("reminder", "").strip()
        original_balance = request.POST.get("original_balance", "")

        if follow_up.status != CollectionFollowUp.Status.ACTIVE:
            messages.error(
                request,
                "El seguimiento ya no está activo."
            )
            return redirect("accounts:account_detail", pk=account.pk)

        if account.balance <= 0:
            messages.error(
                request,
                "La cuenta ya no tiene saldo pendiente."
            )
            return redirect("accounts:account_detail", pk=account.pk)

        try:
            balance_at_generation = Decimal(original_balance)
        except InvalidOperation:
            balance_at_generation = None

        if balance_at_generation != account.balance:
            messages.error(
                request,
                "El saldo de la cuenta ha cambiado. "
                "Genera un nuevo recordatorio antes de enviarlo."
            )
            return redirect("accounts:account_detail", pk=account.pk)

        if not customer.email:
            messages.error(
                request,
                "El cliente no tiene una dirección de email registrada."
            )
            return redirect("accounts:account_detail", pk=account.pk)

        if not reminder:
            messages.error(
                request,
                "El mensaje del recordatorio no puede estar vacío."
            )
            return render(
                request,
                "collections/reminder_review.html",
                {
                    "follow_up": follow_up,
                    "reminder": reminder,
                    "original_balance": original_balance,
                },
            )

        try:
            sender = CollectionReminderEmailSender(follow_up)
            sent_count=sender.send(reminder)
        except Exception:
            messages.error(
                request,
                "No se ha podido enviar el recordatorio por email."
            )
            return render(
                request,
                "collections/reminder_review.html",
                {
                    "follow_up": follow_up,
                    "reminder": reminder,
                    "original_balance": original_balance,
                },
            )
        if sent_count != 1:
            messages.error(
                request,
                "El servidor de correo no ha confirmado el envío."
            )
            return redirect(
                "accounts:account_detail",
                pk=account.pk
            )
        CollectionReminder.objects.create(
            follow_up=follow_up,
            recipient_email=customer.email,
            subject=f"Recordatorio de pago - {account.season.name}",
            message=reminder,
            balance_at_send=account.balance,
        )

        messages.success(
            request,
            f"Recordatorio enviado correctamente a {customer.email}.",
        )

        return redirect(
            "accounts:account_detail",
            pk=account.pk,
        )