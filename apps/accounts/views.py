from django.shortcuts import render
from .models import Account
from ..customers.models import Customer
from apps.seasons.models import Season
from django.views.generic import UpdateView, DetailView, CreateView, ListView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import AccountForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce
from django.db.models import Case, DecimalField, F, Sum, Value, When
from apps.transactions.models import Transaction

# Create your views here.

def closed_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    
    if account.is_closed:
        messages.warning(
            request,
            "La cuenta ya está cerrada."
        )
        return redirect(
        "accounts:account_detail",
        pk=account.pk
        )

    if account.balance != 0:
        messages.error(
            request,
            "No se puede cerrar una cuenta con saldo pendiente."
        )

        return redirect(
        "accounts:account_detail",
        pk=account.pk
        )

    account.is_closed = True
    account.save(update_fields=["is_closed"])


    messages.success(
        request,
        "La cuenta ha sido cerrada correctamente."
    )

    return redirect(
    "accounts:account_detail",
    pk=account.pk
    )

class AccountListView(ListView):
    model=Account
    template_name ="accounts/accounts_list.html"
    context_object_name ="accounts"

    def get_season(self):
        if not hasattr(self, "_selected_season"):
            # Solo entra aquí la PRIMERA vez que se llama a get_season()
            season_id = self.request.GET.get("season")
            if season_id:
                self._selected_season = Season.objects.filter(pk=season_id).first()

            else:
                self._selected_season = Season.objects.filter(is_active=True).first()

        return self._selected_season
    
            


    def get_queryset(self):

        selected_season = self.get_season()

        queryset = Account.objects.filter(
            season=selected_season
        ).select_related("season")

        search = self.request.GET.get("q", "").strip()
        sort = self.request.GET.get("sort", "name_asc")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        queryset = queryset.annotate(
            account_balance = Coalesce(
                Sum(
                    Case(
                        When(
                            transactions__movement_type=Transaction.MovementType.CHARGE,
                            then=F("transactions__amount"),
                        ),
                        When(
                            transactions__movement_type=Transaction.MovementType.PAYMENT,
                            then=-F("transactions__amount"),
                        ),
                        output_field=DecimalField(
                            max_digits=12,
                            decimal_places=2,   
                        ),
                    )
                ),
                Value(0),
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2, 
                ),
            )
        )

        if sort == "name_desc":
            queryset =  queryset.order_by("-name")

        elif sort == "balance_asc":
            queryset = queryset.order_by("account_balance")

        elif sort == "balance_desc":
            queryset = queryset.order_by("-account_balance")

        else:
            queryset = queryset.order_by("name")

        return queryset


    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
    
            active_season = Season.objects.filter(
                is_active = True
            ).first()
    
            selected_season = self.get_season()
    
            context["active_season"] = active_season
            context["selected_season"] = selected_season
            context["seasons"] = Season.objects.all().order_by("start_date")

            return context


    

class AccountDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Account
    permission_required="accounts.view_account"
    context_object_name = "account"
    template_name = "accounts/accounts_detail.html"



class AccountCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Account
    permission_required="accounts.add_account"
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

class AccountUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Account
    permission_required = "accounts.change_account"
    form_class = AccountForm
    template_name = "accounts/account_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "accounts:account_detail",
            kwargs = {"pk": self.object.pk},
        )