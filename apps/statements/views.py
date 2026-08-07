from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from apps.accounts.models import Account

from .services import StatementBuilder

from .pdf import PdfRenderer

from django.views import View

from django.http import HttpResponse

# Create your views here.


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
    
