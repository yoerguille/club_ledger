from django.urls import path

from .views import AccountDetailView, AccountCreateView, AccountUpdateView

app_name = 'accounts'

urlpatterns = [
    path("<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path("customers/<int:customer_pk>/create/", AccountCreateView.as_view(), name="account_create"),
    path("<int:pk>/edit", AccountUpdateView.as_view(), name="account_update"),
    
]
