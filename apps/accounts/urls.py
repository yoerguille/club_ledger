from django.urls import path

from .views import AccountDetailView

app_name = 'accounts'

urlpatterns = [
    path("<int:pk>/", AccountDetailView.as_view(), name="accounts_detail"),
    
]
