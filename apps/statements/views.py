from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from apps.accounts.models import Account

from .services import StatementBuilder

# Create your views here.

class StatementDetailView(TemplateView):

    template_name = "statements/statement_detail.html"

    def get_context_data(self, **kwargs):
        account = get_object_or_404(
            Account,
            pk=self.kwargs["account_pk"],
        )
        
        return StatementBuilder(account).build()
    
