from django.core.mail import EmailMultiAlternatives


class CollectionReminderEmailSender:

    def __init__(self, follow_up):
        self.follow_up = follow_up

    def send(self, message):
        account = self.follow_up.account
        customer = account.customer

        subject = (
            f"Recordatorio de pago - "
            f"{account.name} - {account.season.name}"
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=None,
            to=[customer.email],
        )

        return email.send(fail_silently=False)