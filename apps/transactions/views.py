from django.shortcuts import render
from django.views.generic import CreateView, DeleteView
from .models import Transaction
from .forms import ChargeForm, PaymentForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404 , redirect
from apps.accounts.models import Account
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseNotAllowed

# Create your views here.

class ChargeCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Transaction
    permission_required="transactions.add_transaction"
    form_class = ChargeForm
    template_name = 'transactions/transaction_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.account = get_object_or_404(Account, pk=kwargs["account_pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse("accounts:account_detail", kwargs={"pk": self.account.pk})
    
    def form_valid(self, form):
        transaction = form.save(commit=False)

        transaction.account = self.account
        transaction.movement_type = Transaction.MovementType.CHARGE

        transaction.save()

        messages.success(
            self.request,
            "El cargo se ha registrado correctamente."
        )

        return redirect(self.get_success_url())
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = self.account
        context["title"] = "Registrar pedido"
        return context
        
    



class PaymentCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Transaction
    permission_required="transactions.add_transaction"
    form_class = PaymentForm
    template_name = 'transactions/transaction_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.account = get_object_or_404(Account, pk=kwargs["account_pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse("accounts:account_detail", kwargs={"pk": self.account.pk})
    
    def form_valid(self, form):
        transaction = form.save(commit=False)

        transaction.account = self.account
        transaction.movement_type = Transaction.MovementType.PAYMENT

        transaction.save()

        messages.success(
            self.request,
            "El pago se ha registrado correctamente."
        )

        return redirect(self.get_success_url())
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = self.account
        context["title"] = "Registar pago"
        return  context

class TransactionDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Transaction
    permission_required ="transactions.delete_transaction"

    def get_success_url(self):
        return reverse_lazy("accounts:account_detail", kwargs={"pk": self.object.account.pk})



    
