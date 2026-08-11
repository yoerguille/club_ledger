from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .services import StatementBuilder
from .pdf import PdfRenderer

class StatementEmailSender:

    def __init__(self, account):
        self.account = account

    def send(self, base_url):
        context = StatementBuilder(self.account).build()

        html_content = render_to_string(
            "emails/statements/statement_email.html",
            context,
        )

        text_content = render_to_string(
            "emails/statements/statement_email.txt",
            context,
        )

        pdf = PdfRenderer().render(
            context, 
            base_url,
            )

        customer = context["customer"]
        season = context["season"]

        subject = (
            f"Estado de cuenta - "
            f"{season.name}"
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=None,
            to=[customer.email],
        )

        email.attach_alternative(
            html_content,
            "text/html",
        )

        email.attach(
            f"estado_cuenta_{self.account.pk}.pdf",
            pdf,
            "application/pdf"
        )

        email.send()

        