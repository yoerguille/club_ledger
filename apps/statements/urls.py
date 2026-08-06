from django.urls import path

from .views import StatementDetailView

app_name = 'statements'

urlpatterns = [
    path("accounts/<int:account_pk>/", StatementDetailView.as_view(), name="statement_detail"),
]