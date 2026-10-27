from django.test import TestCase
from apps.seasons.models import Season
from django.core.exceptions import ValidationError
from apps.seasons.services.season_service import SeasonService
from apps.seasons.services.season_service import (
    SeasonChangeConfirmationRequired,
)
from apps.accounts.models import Account
from apps.customers.models import Customer
from apps.transactions.models import Transaction
from apps.seasons.services.season_stats import (
    get_season_pending_balances,
)

from decimal import Decimal
from datetime import date
from django.urls import reverse
from apps.seasons.services.season_stats import get_season_stats

# Create your tests here.
class SeasonPendingBalancesTests(TestCase):

    def setUp(self):
        self.season = Season.objects.create(
            name="2026/2027",
            start_date=date(2026, 9, 1),
            end_date=date(2027, 6, 30),
            is_active=True,
        )

        # Crear tres clientes y sus cuentas
        self.accounts = []

        for name in ["Club A", "Club B", "Club C"]:
            customer = Customer.objects.create(name=name)

            account = Account.objects.create(
                customer=customer,
                season=self.season,
                name="Cuenta general",
            )

            self.accounts.append(account)

    def test_get_season_stats(self):
        # Arrange
        account_a, account_b, account_c = self.accounts

        movements = [
            (account_a, Transaction.MovementType.CHARGE, "300.00"),
            (account_a, Transaction.MovementType.PAYMENT, "100.00"),
            (account_b, Transaction.MovementType.CHARGE, "100.00"),
            (account_b, Transaction.MovementType.PAYMENT, "150.00"),
            (account_c, Transaction.MovementType.CHARGE, "250.00"),
        ]

        for account, movement_type, amount in movements:
            Transaction.objects.create(
                account=account,
                movement_type=movement_type,
                date=date(2026, 10, 1),
                amount=Decimal(amount),
                description="Movimiento de prueba",
                payment_method=(
                    Transaction.PaymentMethod.TRANSFER
                    if movement_type == Transaction.MovementType.PAYMENT
                    else None
                ),
            )

        # Act
        stats = get_season_stats(self.season)

        # Assert
        self.assertEqual(stats["account_count"], 3)
        self.assertEqual(stats["transaction_count"], 5)

        self.assertEqual(stats["total_charges"], Decimal("650.00"))
        self.assertEqual(stats["total_payments"], Decimal("250.00"))
        self.assertEqual(stats["total_balance"], Decimal("400.00"))

        self.assertEqual(stats["pending_accounts_count"], 2)
        self.assertEqual(stats["total_pending"], Decimal("450.00"))

    def test_pending_balances_only_include_positive_accounts(self):

        # Arrange
        account_a, account_b, account_c = self.accounts

        movements = [
            (account_a, Transaction.MovementType.CHARGE, "300.00"),
            (account_a, Transaction.MovementType.PAYMENT, "100.00"),
            (account_b, Transaction.MovementType.CHARGE, "100.00"),
            (account_b, Transaction.MovementType.PAYMENT, "150.00"),
            (account_c, Transaction.MovementType.CHARGE, "250.00"),
        ]

        for account, movement_type, amount in movements:
            Transaction.objects.create(
                account=account,
                movement_type=movement_type,
                date=date(2026, 10, 1),
                amount=Decimal(amount),
                description="Movimiento de prueba",
                payment_method=(
                    Transaction.PaymentMethod.TRANSFER
                    if movement_type == Transaction.MovementType.PAYMENT
                    else None
                ),
            )

        # Act
        result = get_season_pending_balances(self.season)

        # Assert
        self.assertEqual(
            result["pending_accounts_count"],
            2,
        )

        self.assertEqual(
            result["total_pending"],
            Decimal("450.00"),
        )

class SeasonChangeTests(TestCase):

    def setUp(self):
        self.active_season = Season.objects.create(
            name="2025/2026",
            start_date=date(2025, 9, 1),
            end_date=date(2026, 6, 30),
            is_active=True,
        )

    def test_create_season_without_confirmation(self):

        # Act & Assert: debe solicitar confirmación
        with self.assertRaises(SeasonChangeConfirmationRequired):
            SeasonService.create_season(
                name="2026/2027",
                start_date=date(2026, 9, 1),
                end_date=date(2027, 6, 30),
            )

        # Assert: la temporada original sigue activa
        self.active_season.refresh_from_db()

        self.assertTrue(self.active_season.is_active)
        self.assertEqual(Season.objects.count(), 1)
        self.assertEqual(
            Season.objects.filter(is_active=True).count(),
            1,
        )

    def test_create_season_with_confirmation(self):
        # Act
        new_season = SeasonService.create_season(
            name="2026/2027",
            start_date=date(2026, 9, 1),
            end_date=date(2027, 6, 30),
            confirm_change=True,
            expected_active_season_id=self.active_season.pk,
        )

        # Assert
        self.active_season.refresh_from_db()
        new_season.refresh_from_db()

        self.assertFalse(self.active_season.is_active)
        self.assertTrue(new_season.is_active)

        self.assertEqual(Season.objects.count(), 2)
        self.assertEqual(
            Season.objects.filter(is_active=True).count(),
            1,
        )
    def test_create_season_with_stale_confirmation(self):
        # Arrange: ID de una temporada distinta a la activa
        wrong_season_id = self.active_season.pk + 999

        # Act & Assert: debe rechazar la confirmación
        with self.assertRaises(ValidationError):
            SeasonService.create_season(
                name="2026/2027",
                start_date=date(2026, 9, 1),
                end_date=date(2027, 6, 30),
                confirm_change=True,
                expected_active_season_id=wrong_season_id,
            )

        # Assert: no debe modificar las temporadas
        self.active_season.refresh_from_db()

        self.assertTrue(self.active_season.is_active)
        self.assertEqual(Season.objects.count(), 1)

    def test_create_season_with_duplicate_name(self):
        # Arrange: desactivar la temporada existente
        self.active_season.is_active = False
        self.active_season.save()

        # Act & Assert: intentar crear otra con el mismo nombre
        with self.assertRaises(ValidationError):
            SeasonService.create_season(
                name="2025/2026",
                start_date=date(2025, 9, 1),
                end_date=date(2026, 6, 30),
            )

        # Assert: no se ha creado otra temporada
        self.assertEqual(Season.objects.count(), 1)
        self.assertFalse(
            Season.objects.get(pk=self.active_season.pk).is_active
        )


class SeasonServiceTests(TestCase):
    def test_create_first_season_activates_it(self):
        # Arrange: preparar los datos
        name = "2026/2027"
        start_date = date(2026, 9, 1)
        end_date = date(2027, 6, 30)

        # Act: ejecutar la funcionalidad
        season = SeasonService.create_season(
            name=name,
            start_date=start_date,
            end_date=end_date,
        )

        # Assert: comprobar el resultado
        self.assertTrue(season.is_active)
        self.assertEqual(season.name, name)
        self.assertEqual(Season.objects.count(), 1)
        self.assertEqual(
            Season.objects.filter(is_active=True).count(),
            1,
        )
    def test_create_season_with_invalid_dates(self):
        with self.assertRaises(ValidationError):
            SeasonService.create_season(
                name="2026/2027",
                start_date=date(2027, 6, 30),
                end_date=date(2026, 9, 1),
            )

        self.assertEqual(Season.objects.count(), 0)