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
from apps.collection.models import CollectionFollowUp

# Create your views here.

class ChargeCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Transaction
    permission_required="transactions.add_transaction"
    form_class = ChargeForm
    template_name = 'transactions/transaction_form.html'


    def dispatch(self, request, *args, **kwargs):
        self.account = get_object_or_404(Account, pk=kwargs["account_pk"])

        if self.account.is_closed:
            messages.error(
                self.request,
                "No se puede registrar un cargo en una cuenta cerrada."
            )
            return redirect("accounts:account_detail", pk=self.account.pk)

        has_active_followup = self.account.collection_followups.filter(
            status=CollectionFollowUp.Status.ACTIVE,
        ).exists()

        if has_active_followup:
            messages.error(
                self.request,
                "No se puede registrar un nuevo cargo mientras la cuenta tenga un seguimiento de cobro activo."
            )
            return redirect("accounts:account_detail", pk=self.account.pk)

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

        if self.account.balance <= 0:
            active_follow_up = self.account.active_collection_follow_up
            if active_follow_up:
                active_follow_up.status = CollectionFollowUp.Status.COMPLETED
                active_follow_up.save(update_fields=["status"])
                
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



    
