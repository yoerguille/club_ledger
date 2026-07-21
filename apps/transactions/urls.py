from django.urls import path

from .views import ChargeCreateView, PaymentCreateView

app_name = 'transactions'

urlpatterns = [
    path("account/<int:account_pk>/charge/", ChargeCreateView.as_view(), name="charge_create"),
    path("account/<int:account_pk>/payment/", PaymentCreateView.as_view(), name="payment_create"),
]
