from django.urls import path

from apps.accounts.api_views import AccountCreateAPIView


urlpatterns = [
    path(
        "customers/<int:customer_pk>/new-account/",
        AccountCreateAPIView.as_view(),
        name="api_account_create",
    ),

]