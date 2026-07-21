from django.shortcuts import render
from django.views.generic import CreateView
from .models import Transaction
from .forms import ChargeForm, PaymentForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404 
from apps.accounts.models import Account

# Create your views here.

class ChargeCreateView(CreateView):
    model = Transaction

    form_class = ChargeForm
    template_name = 'transactions/transaction_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.account = get_object_or_404(Account, pk=kwargs["account_pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.account = self.account
        form.instance.movement_type = Transaction.MovementType.CHARGE
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("accounts:account_detail", kwargs={"pk": self.account.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = self.account
        context["title"] = "Registrar pedido"
        return context
        
    



class PaymentCreateView(CreateView):
    model = Transaction

    form_class = PaymentForm
    template_name = 'transactions/transaction_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.account = get_object_or_404(Account, pk=kwargs["account_pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.account = self.account
        form.instance.movement_type = Transaction.MovementType.PAYMENT
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("accounts:account_detail", kwargs={"pk": self.account.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = self.account
        context["title"] = "Registar pago"
        return  context
    
