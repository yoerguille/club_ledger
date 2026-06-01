from django.shortcuts import render
from .models import Account
from django.views.generic import DetailView

# Create your views here.

class AccountDetailView(DetailView):
    model = Account
    context_object_name = "account"
    template_name = "accounts/accounts_detail.html"
