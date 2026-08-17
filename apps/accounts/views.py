from django.shortcuts import render
from .models import Account
from ..customers.models import Customer
from django.views.generic import DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import AccountForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    context_object_name = "account"
    template_name = "accounts/accounts_detail.html"


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    context_object_name = "account"
    template_name = "accounts/account_form.html"
    form_class=AccountForm

    def dispatch(self, request, *args, **kwargs):
        self.customer = get_object_or_404(
            Customer,
            pk=kwargs["customer_pk"],
        )

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["customer"] = self.customer

        return kwargs 

    def form_valid(self, form):
        account = form.save(commit=False)
        account.customer = self.customer
        account.save()

        messages.success(
            self.request,
            "La cuenta se ha creado correctamente"
        )
        
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            "customers:customer_detail",
            kwargs={"pk" : self.customer.pk},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer"] = self.customer
        context["title"] = "Nueva cuenta"

        return context