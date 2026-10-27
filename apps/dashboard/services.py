from django.db.models import Case, DecimalField, F, Sum, Value, When
from django.db.models.functions import Coalesce

from apps.accounts.models import Account
from apps.customers.models import Customer
from apps.seasons.models import Season
from apps.transactions.models import Transaction


from decimal import Decimal

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