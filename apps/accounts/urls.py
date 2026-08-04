from django.urls import path

from .views import AccountDetailView, AccountCreateView

app_name = 'accounts'

urlpatterns = [
    path("<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path("customers/<int:customer_pk>/create/", AccountCreateView.as_view(), name="account_create"),
    
]
