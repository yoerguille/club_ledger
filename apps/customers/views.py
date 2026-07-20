from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Customer
from .forms import CustomerForm
from django.urls import reverse_lazy

# Create your views here.
class CustomerListView(ListView):
    model = Customer
    template_name = "customers/customers_list.html"
    context_object_name = "customers"

class CustomerDetailView(DetailView):
    model = Customer
    template_name ="customers/customers_detail.html"
    context_object_name = 'customer'

class CustomerCreateView(CreateView):
    model = Customer

    form_class = CustomerForm
    template_name = 'customers/customer_form.html'

    success_url = reverse_lazy("customers:customer_list")