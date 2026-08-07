from django.urls import path

from .views import StatementDetailView, StatementPdfView

app_name = 'statements'

urlpatterns = [
    path("accounts/<int:account_pk>/", StatementDetailView.as_view(), name="statement_detail"),
    path("accounts/<int:account_pk>/pdf/", StatementPdfView.as_view(), name="statement_pdf"),
]