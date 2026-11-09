from django.urls import path

from .views import StatementDetailView, StatementPdfView, StatementEmailView, StatementInfoEmailView

app_name = 'statements'

urlpatterns = [
    path("accounts/<int:account_pk>/", StatementDetailView.as_view(), name="statement_detail"),
    path("accounts/<int:account_pk>/pdf/", StatementPdfView.as_view(), name="statement_pdf"),
    path("accounts/<int:account_pk>/email/", StatementEmailView.as_view(), name="statement_email"),
    path("accounts/<int:account_pk>/info-email/", StatementInfoEmailView.as_view(), name="statement_info_email"),
]