from django.urls import path

from apps.transactions.api_views import PaymentCreateAPIView


urlpatterns = [
    path(
        "accounts/<int:account_pk>/payments/",
        PaymentCreateAPIView.as_view(),
        name="api_payment_create",
    ),
]