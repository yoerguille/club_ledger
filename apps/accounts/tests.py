from django.test import TestCase
from apps.customers.models import Customer
from apps.seasons.models import Season
from apps.accounts.models import Account
from apps.accounts.services import register_new_account
from apps.accounts.services import AccountCloseService
from apps.transactions.models import Transaction
from django.core.exceptions import ValidationError

from decimal import Decimal
from datetime import date
from django.urls import reverse

# Create your tests here.
class AccountCloseServiceTests(TestCase):
    def setUp(self):
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

    def test_close_account_with_zero_balance(self):

        self.assertEqual(self.account.balance, Decimal("0.00"))

        # ACT
        AccountCloseService.close(self.account)

        # ASSERT
        self.account.refresh_from_db()
        self.assertTrue(self.account.is_closed)

    def test_cannot_close_account_with_debt(self):

        transaction = Transaction.objects.create(
            account = self.account,
            movement_type = Transaction.MovementType.CHARGE,
            date = date(2026,10,23),
            amount =Decimal("150.00"),
            description = "Test de prueba",
        )
        self.assertEqual(self.account.balance, Decimal("150.00"))

        # ACT + ASSERT
        with self.assertRaises(ValidationError):
            AccountCloseService.close(self.account)

        # ASSERT: comprobar que la cuenta sigue abierta
        self.account.refresh_from_db()
        self.assertFalse(self.account.is_closed)

    def test_cannot_close_account_already_closed(self):
        self.assertEqual(self.account.balance, Decimal("0.00"))
        
        # ACT
        AccountCloseService.close(self.account)

        # ASSERT
        self.account.refresh_from_db()
        self.assertTrue(self.account.is_closed)

        with self.assertRaises(ValidationError):
            AccountCloseService.close(self.account)

        self.account.refresh_from_db()
        self.assertTrue(self.account.is_closed)

    def test_close_account_rejects_get_request(self):
        url = reverse(
            "accounts:account_close",
            args=[self.account.pk]
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)
        self.account.refresh_from_db()
        self.assertFalse(self.account.is_closed)

class AccountCreateServiceTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Club Deportivo Test"
        )

        self.season = Season.objects.create(
            name="2026/2027",
            start_date=date(2026, 9, 1),
            end_date=date(2027, 6, 30),
            is_active=True,
        )

    def test_register_new_account_success(self):
        account = register_new_account(
            customer=self.customer,
            season=self.season,
            name="Cuenta de Prueba",
            notes="Notas de prueba"
        )


        self.assertIsInstance(account, Account)

    def test_register_new_account_fails_for_inactive_season(self):
        self.season.is_active = False
        self.season.save()

        with self.assertRaises(ValidationError):
            register_new_account(
                customer=self.customer,
                season=self.season,
                name="Cuenta de Prueba",
                notes="Notas de prueba"
            )


class AccountCreateWebTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Permission

        user = get_user_model().objects.create_user(username="account_creator")
        user.user_permissions.add(Permission.objects.get(
            content_type__app_label="accounts", codename="add_account"
        ))
        self.client.force_login(user)
        self.customer = Customer.objects.create(name="Club")
        self.url = reverse("accounts:account_create", args=[self.customer.pk])

    def test_account_uses_active_season(self):
        season = Season.objects.create(
            name="Activa", start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31), is_active=True,
        )
        response = self.client.post(self.url, {"name": "General"})
        self.assertRedirects(response, reverse("customers:customer_detail", args=[self.customer.pk]),
                             fetch_redirect_response=False)
        account = Account.objects.get(customer=self.customer, name="General")
        self.assertEqual(account.season, season)

    def test_missing_active_season_rejects_account(self):
        response = self.client.post(self.url, {"name": "General"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("No hay ninguna temporada activa", str(response.context["form"].non_field_errors()))
        self.assertFalse(Account.objects.exists())
