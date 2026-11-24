from uuid import uuid4
from django.core.exceptions import ValidationError
from apps.collection.delivery import deliver, report_delivery
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib import messages

from apps.accounts.models import Account

from .services import StatementBuilder

from .pdf import PdfRenderer
from .email import StatementEmailSender

from django.views import View

from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class StatementEmailView(LoginRequiredMixin, View):

    def post(self, request, account_pk):

        account = get_object_or_404(
            Account,
            pk=account_pk,
        )

        if account.active_collection_follow_up:

            messages.error(
                request,
                "Esta cuenta ya tiene un seguimiento de cobro activo. "
                "Cancélalo antes de iniciar uno nuevo."
            )
            return redirect(
                "accounts:account_detail",
                pk=account.pk,
            )

        if account.balance <= 0:
            
            messages.error(
                request,
                "Esta cuenta no tiene saldo pendiente. "
                "No se puede enviar un estado de cuenta."
            )
            return redirect(
                "accounts:account_detail",
                pk=account.pk,
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

        try:
            status = deliver(account.pk, request.POST.get("delivery_token"), base_url=request.build_absolute_uri("/"))
        except ValidationError as error:
            messages.error(request, " ".join(error.messages))
        else:
            report_delivery(request, status)

        return redirect(
            "accounts:account_detail",
            pk=account.pk,
        )

class StatementInfoEmailView(LoginRequiredMixin, TemplateView):

    def post(self, request, account_pk):

        account = get_object_or_404(
            Account,
            pk=account_pk,
        )

        customer  = account.customer

        if not customer.email:
            messages.error(
                request,
                "El cliente no tiene una dirección de email registrada."
            )

            return redirect("accounts:account_list")

        base_url = request.build_absolute_uri("/")

        StatementEmailSender(account).send(
            base_url=base_url,
        )

        messages.success(
            request,
            f"Email enviado correctamente a {customer.email}.",
        )

        return redirect(
            "accounts:account_detail",
            pk=account.pk,
        )

class StatementPdfView(LoginRequiredMixin, View):

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

class StatementDetailView(LoginRequiredMixin, TemplateView):

    template_name = "statements/statement_detail.html"

    def get_context_data(self, **kwargs):
        account = get_object_or_404(
            Account,
            pk=self.kwargs["account_pk"],
        )

        builder = StatementBuilder(account)
        
        return {**builder.build(), "delivery_token": uuid4()}
    
