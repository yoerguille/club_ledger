from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Customer

# Create your views here.
class CustomerListView(ListView):
    model = Customer
    template_name = "customers/customers_list.html"
    context_object_name = "customers"

class CustomerDetailView(DetailView):
    model = Customer
    template_name ="customers/customers_detail.html"
    context_object_name = 'customer'