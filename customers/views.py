from django.shortcuts import render
from django.views.generic import ListView
from .models import Customer

# Create your views here.
class CustomerListView(ListView):
    model = Customer
    template_name = "customers/customers_list.html"
    context_object_name = "customers"