from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib import messages

from apps.accounts.models import Account

from .services import StatementBuilder

from .pdf import PdfRenderer
from .email import StatementEmailSender

from django.views import View

from django.http import HttpResponse

# Create your views here.


class StatementEmailView(View):

    def post(self, request, account_pk):

        account = get_object_or_404(
            Account,
            pk=account_pk,
        )

        customer = account.customer

        if not customer.email:

            messages.error(
                request,
                "El cliente no tiene una dirección de email registrada."
            )

            return redirect(
                "accounts:account_detail",
                pk=account.pk,
            )

        base_url = request.build_absolute_uri("/")

        StatementEmailSender(account).send(
            base_url=base_url,
        )

        messages.success(
            request,
            f"Estado de cuenta enviado correctamente a {customer.email}.",
        )

        return redirect(
            "accounts:account_detail",
            pk=account.pk,
        )
            


class StatementPdfView(View):

    def get(self, request, account_pk):

        account = get_object_or_404(
            Account,
            pk=account_pk,
        )

        builder = StatementBuilder(account)

        context = builder.build()

        pdf = PdfRenderer().render(
            context=context,
            base_url=request.build_absolute_uri("/"),
        )

        response = HttpResponse(
            pdf,
            content_type="application/pdf",
        )

        response["Content-Disposition"] = (
            f'attachment; filename="estado_cuenta_{account.pk}.pdf"'
        )

        return response

class StatementDetailView(TemplateView):

    template_name = "statements/statement_detail.html"

    def get_context_data(self, **kwargs):
        account = get_object_or_404(
            Account,
            pk=self.kwargs["account_pk"],
        )

        builder = StatementBuilder(account)
        
        return builder.build()
    
