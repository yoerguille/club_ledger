from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.accounts.models import Account
from apps.accounts.services import AccountCloseService
from apps.customers.models import Customer
from apps.seasons.models import Season
from apps.transactions.services import delete_transaction, register_charge, register_payment


class ClosedAccountTests(TestCase):
    def test_closed_account_rejects_changes_even_with_stale_instance(self):
        season = Season.objects.create(name="Test", start_date=date(2026, 1, 1), end_date=date(2026, 12, 31))
        account = Account.objects.create(customer=Customer.objects.create(name="Club"), season=season, name="Cuenta")
        data = dict(account=account, date=date(2026, 3, 1), description="Movimiento", amount=Decimal("25.00"))
        charge = register_charge(**data)
        register_payment(payment_method="cash", **data)
        AccountCloseService.close(Account.objects.get(pk=account.pk))

        with self.assertRaises(ValidationError):
            register_payment(payment_method="cash", **data)
        with self.assertRaises(ValidationError):
            register_charge(**data)
        with self.assertRaises(ValidationError):
            delete_transaction(charge)

        with self.assertRaises(IntegrityError), transaction.atomic():
            account.transactions.update(amount=Decimal("10.00"))
        with self.assertRaises(IntegrityError), transaction.atomic():
            account.transactions.all().delete()

        account.refresh_from_db()
        self.assertTrue(account.is_closed)
        self.assertEqual(account.balance, Decimal("0.00"))
        self.assertEqual(account.transactions.count(), 2)
