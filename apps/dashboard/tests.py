from django.test import TestCase
from apps.dashboard.services import get_monthly_transactions
from apps.transactions.models import Transaction
from apps.customers.models import Customer
from apps.seasons.models import Season
from apps.accounts.models import Account
from datetime import date
from decimal import Decimal


# Create your tests here.

class SeasonMonthlyTransactionsTests(TestCase):

    def setUp(self):
        self.season = Season.objects.create(
            name="2026/2027",
            start_date=date(2026, 9, 1),
            end_date=date(2027, 6, 30),
            is_active=True,
        )

        self.customer = Customer.objects.create(
            name="Club de prueba",
        )

        self.account = Account.objects.create(
            customer=self.customer,
            season=self.season,
            name="Cuenta general",
        )

    def test_monthly_transactions_grouped_by_month(self):

        # Arrange: movimientos de septiembre
        self.create_transaction(
            Transaction.MovementType.CHARGE,
            "300.00",
            date(2026, 9, 5),
        )

        self.create_transaction(
            Transaction.MovementType.PAYMENT,
            "100.00",
            date(2026, 9, 15),
        )

        # Movimientos de octubre
        self.create_transaction(
            Transaction.MovementType.CHARGE,
            "500.00",
            date(2026, 10, 3),
        )

        self.create_transaction(
            Transaction.MovementType.PAYMENT,
            "200.00",
            date(2026, 10, 20),
        )

        # Act
        result = get_monthly_transactions(self.season)

        # Assert
        self.assertEqual(len(result), 2)

        self.assertEqual(result[0]["month"], date(2026, 9, 1))
        self.assertEqual(result[0]["charges"], Decimal("300.00"))
        self.assertEqual(result[0]["payments"], Decimal("100.00"))

        self.assertEqual(result[1]["month"], date(2026, 10, 1))
        self.assertEqual(result[1]["charges"], Decimal("500.00"))
        self.assertEqual(result[1]["payments"], Decimal("200.00"))

    def create_transaction(self, movement_type, amount, movement_date):
        return Transaction.objects.create(
            account=self.account,
            movement_type=movement_type,
            date=movement_date,
            amount=Decimal(amount),
            description="Movimiento de prueba",
            payment_method=(
                Transaction.PaymentMethod.TRANSFER
                if movement_type == Transaction.MovementType.PAYMENT
                else None
            ),
        )

    def test_monthly_transactions_include_empty_months(self):
        # Septiembre
        self.create_transaction(
            Transaction.MovementType.CHARGE,
            "300.00",
            date(2026, 9, 5),
        )

        # Noviembre
        self.create_transaction(
            Transaction.MovementType.PAYMENT,
            "200.00",
            date(2026, 11, 10),
        )

        # Act
        result = get_monthly_transactions(self.season)

        # Assert
        self.assertEqual(len(result), 3)

        october = result[1]

        self.assertEqual(october["month"], date(2026, 10, 1))
        self.assertEqual(october["charges"], Decimal("0.00"))
        self.assertEqual(october["payments"], Decimal("0.00"))

