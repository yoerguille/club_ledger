from django.db.models import Case, DecimalField, F, Sum, Value, When, Q
from django.db.models.functions import Coalesce
from django.db.models.functions import TruncMonth

from apps.accounts.models import Account
from apps.customers.models import Customer
from apps.seasons.models import Season
from apps.transactions.models import Transaction


from decimal import Decimal
from datetime import date

from apps.customers.models import Customer
from apps.seasons.models import Season
from apps.seasons.services.season_stats import get_season_stats


def get_dashboard_stats():
    """
    Devuelve las estadísticas generales del dashboard,
    utilizando las estadísticas de la temporada activa.
    """

    total_customers = Customer.objects.filter(
        is_active=True
    ).count()

    active_season = Season.objects.filter(
        is_active=True
    ).first()

    # Si no existe una temporada activa
    if active_season is None:
        return {
            "total_customers": total_customers,
            "active_season": None,
            "total_accounts": 0,
            "total_transactions": 0,
            "total_payments": Decimal("0.00"),
            "total_charges": Decimal("0.00"),
            "total_balance": Decimal("0.00"),
        }

    # Reutilizar los cálculos económicos
    stats = get_season_stats(active_season)

    return {
        "total_customers": total_customers,
        "active_season": active_season,
        "total_accounts": stats["account_count"],
        "total_transactions": stats["transaction_count"],
        "total_payments": stats["total_payments"],
        "total_charges": stats["total_charges"],
        "total_balance": stats["total_balance"],
    }

def get_monthly_transactions(season):
    """
    Devuelve el total de cargos y pagos agrupados por mes
    para una temporada determinada.
    """

    if season is None:
        return []

    monthly_data = list(
        Transaction.objects.filter(
            account__season=season
        )
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            charges=Sum(
                "amount",
                filter=Q(
                    movement_type=Transaction.MovementType.CHARGE
                ),
                default=0,
            ),
            payments=Sum(
                "amount",
                filter=Q(
                    movement_type=Transaction.MovementType.PAYMENT
                ),
                default=0,
            ),
        )
        .order_by("month")
    )
    return fill_missing_months(monthly_data)

def fill_missing_months(monthly_data):
    """
    Completa los meses sin movimientos entre
    el primer y el último mes registrado.
    """

    if not monthly_data:
        return []

    months = {
        item["month"]: item
        for item in monthly_data
    }

    current = monthly_data[0]["month"]
    last = monthly_data[-1]["month"]

    result = []

    while current <= last:
        result.append(
            months.get(
                current,
                {
                    "month": current,
                    "charges": Decimal("0.00"),
                    "payments": Decimal("0.00"),
                },
            )
        )

        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)

    return result