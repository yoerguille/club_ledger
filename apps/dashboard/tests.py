from django.test import TestCase
from apps.dashboard.services import get_monthly_transactions, get_account_balance_distribution
from apps.transactions.models import Transaction
from apps.customers.models import Customer
from apps.seasons.models import Season
from apps.accounts.models import Account
from apps.accounts.services import AccountCloseService
from datetime import date
from decimal import Decimal


# Create your tests here.

class AccountsDistributionTests(TestCase):
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

    def test_new_account_(self):
        result = get_account_balance_distribution(self.season)

        self.assertEqual(result['balance_0'], 1)
        self.assertEqual(result['pending'], 0)
        self.assertEqual(result['closed'], 0)
        self.assertEqual(result['negative_balance'], 0)

    def test_account_with_zero_balance(self):
        self.create_transaction(
            Transaction.MovementType.CHARGE,
            "300.00",
            date(2026, 9, 5),
        )
        self.create_transaction(
            Transaction.MovementType.PAYMENT,
            "300.00",
            date(2026, 9, 15),
        )

        result = get_account_balance_distribution(self.season)

        self.assertEqual(result['balance_0'], 1)
        self.assertEqual(result['pending'], 0)
        self.assertEqual(result['closed'], 0)
        self.assertEqual(result['negative_balance'], 0)

    def test_closed_account(self):
        AccountCloseService.close(self.account)
        result = get_account_balance_distribution(self.season)

        self.assertEqual(result['balance_0'], 0)
        self.assertEqual(result['pending'], 0)
        self.assertEqual(result['closed'], 1)
        self.assertEqual(result['negative_balance'], 0)

    def test_pending_account(self):
        self.create_transaction(
            Transaction.MovementType.CHARGE,
            "300.00",
            date(2026, 9, 5),
        )

        result = get_account_balance_distribution(self.season)
        
        self.assertEqual(result['balance_0'], 0)
        self.assertEqual(result['pending'], 1)
        self.assertEqual(result['closed'], 0)
        self.assertEqual(result['negative_balance'], 0)

    def test_negative_balance_account(self):
        self.create_transaction(
            Transaction.MovementType.CHARGE,
            "300.00",
            date(2026, 9, 5),
        )

        self.create_transaction(
            Transaction.MovementType.PAYMENT,
            "400.00",
            date(2026, 9, 15),
        )

        result = get_account_balance_distribution(self.season)
        
        self.assertEqual(result['balance_0'], 0)
        self.assertEqual(result['pending'], 0)
        self.assertEqual(result['closed'], 0)
        self.assertEqual(result['negative_balance'], 1)

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
    def create_transaction_for_differents_accounts(self, movement_type, amount, movement_date, account):
        return Transaction.objects.create(
            account=account,
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

    def test_various_accounts_with_diferent_balance(self):
        self.account2 = Account.objects.create(
            customer=self.customer,
            season=self.season,
            name="Cuenta general",
        )
        self.account3 = Account.objects.create(
            customer=self.customer,
            season=self.season,
            name="Cuenta general",
        )
        self.account4 = Account.objects.create(
            customer=self.customer,
            season=self.season,
            name="Cuenta general",
        )
        self.account5 = Account.objects.create(
            customer=self.customer,
            season=self.season,
            name="Cuenta general",
        )

        #Cuenta setup: Nueva cuenta

        #Cuenta 2: Saldo zero
        self.create_transaction_for_differents_accounts(
            Transaction.MovementType.CHARGE,
            "300.00",
            date(2026, 9, 5),
            self.account2,
        )
        self.create_transaction_for_differents_accounts(
            Transaction.MovementType.PAYMENT,
            "300.00",
            date(2026, 9, 15),
            self.account2,
        )

        #Cuenta 3: Saldo pendiente
        self.create_transaction_for_differents_accounts(
            Transaction.MovementType.CHARGE,
            "300.00",
            date(2026, 9, 5),
            self.account3,
        )

        #Cuenta 4: Saldo negativo
        self.create_transaction_for_differents_accounts(
            Transaction.MovementType.CHARGE,
            "300.00",
            date(2026, 9, 5),
            self.account4,
        )
        self.create_transaction_for_differents_accounts(
            Transaction.MovementType.PAYMENT,
            "400.00",
            date(2026, 9, 15),
            self.account4,
        )

        #Cuenta 5: Cuenta cerrada
        AccountCloseService.close(self.account5)


        result = get_account_balance_distribution(self.season)
        self.assertEqual(result['balance_0'], 2)
        self.assertEqual(result['pending'], 1)
        self.assertEqual(result['closed'], 1)
        self.assertEqual(result['negative_balance'], 1)
    

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

