from django.test import TestCase
from apps.customers.models import Customer
from apps.seasons.models import Season
from apps.accounts.models import Account
from apps.statements.views import StatementInfoEmailView
from datetime import date
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.
class StatementInfoEmailViewTests(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.client.force_login(self.user)

        self.customer = Customer.objects.create(
            name="Club Deportivo Test"
        )

        self.season = Season.objects.create(
            name="2026/2027",
            start_date=date(2026, 9, 1),
            end_date=date(2027, 6, 30)
        )

        self.account = Account.objects.create(
            customer=self.customer,
            season=self.season,
            name="Cuenta General"
        )

    @patch("apps.statements.email.StatementEmailSender.send")
    def test_send_email_to__no_email_account(self, mock_send):

        url = reverse(
            "statements:statement_info_email",
            kwargs={"account_pk":self.account.pk}
        )

        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse(
                "accounts:account_list",
            )
        )

        mock_send.assert_not_called()