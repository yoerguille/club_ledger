from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Customer
from apps.seasons.models import Season
from apps.accounts.models import Account
from .forms import CustomerForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "customers/customers_list.html"
    context_object_name = "customers"

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
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


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer

    form_class = CustomerForm
    template_name = 'customers/customer_form.html'

    success_url = reverse_lazy("customers:customer_list")

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer

    form_class = CustomerForm
    template_name = 'customers/customer_form.html'

    def get_success_url(self):
        return reverse_lazy(
            "customers:customer_detail",
            kwargs = {"pk": self.object.pk},
        )