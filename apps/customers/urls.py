from django.urls import path

from .views import CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView

app_name = 'customers'

urlpatterns = [
    path("", CustomerListView.as_view(), name="customer_list"),
    path("<int:pk>/", CustomerDetailView.as_view(), name="customer_detail"),
    path("create/", CustomerCreateView.as_view(), name="customer_create"),
    path("<int:pk>/edit", CustomerUpdateView.as_view(), name="customer_update"),
    
]
