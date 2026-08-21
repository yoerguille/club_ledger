from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Customer
from apps.seasons.models import Season
from apps.accounts.models import Account
from apps.transactions.models import Transaction
from .forms import CustomerForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.db.models import Case, DecimalField, F, Sum, Value, When
from django.db.models.functions import Coalesce

# Create your views here.
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "customers/customers_list.html"
    context_object_name = "customers"

    def get_queryset(self):
        queryset= super().get_queryset()

        search = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        if status == "active":
            queryset = queryset.filter(
                is_active=True
            )

        elif status == "inactive":
                    queryset = queryset.filter(
                        is_active=False
                    )


        queryset = queryset.annotate(
             customer_balance = Coalesce(
                  Sum(
                       Case(
                            When(
                                 accounts__transactions__movement_type=Transaction.MovementType.CHARGE,
                                 then=F("accounts__transactions__amount"),
                            ),
                            When(
                                 accounts__transactions__movement_type=Transaction.MovementType.PAYMENT,
                                 then=-F("accounts__transactions__amount"),
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

        for customer in queryset:
            print(
            customer.name,
            "->",
            customer.customer_balance
            )

        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["customers_count"] = self.get_queryset().count()

        return context

class CustomerDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Customer
    permission_required = "customers.view_customer"
    template_name ="customers/customers_detail.html"
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        active_season = Season.objects.filter(
            is_active = True
        ).first()

        season_id = self.request.GET.get("season")

        if season_id:
            selected_season = Season.objects.filter(
                pk=season_id
            ).first()

        else:
            selected_season = active_season

        accounts = Account.objects.filter(
            customer = self.object,
            season = selected_season,
        ).select_related(
            "season",
        )

        context["active_season"] = active_season
        context["selected_season"] = selected_season
        context["seasons"] = Season.objects.filter(
            accounts__customer=self.object
        ).distinct().order_by("-name")
        context["accounts"] = accounts

        return context


class CustomerCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Customer
    permission_required="customers.add_customer"
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'

    success_url = reverse_lazy("customers:customer_list")

class CustomerUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Customer
    permission_required="customers.change_customer"
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'

    def get_success_url(self):
        return reverse_lazy(
            "customers:customer_detail",
            kwargs = {"pk": self.object.pk},
        )