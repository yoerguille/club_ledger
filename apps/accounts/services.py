from django.db import transaction
from apps.accounts.models import Account

from django.core.exceptions import ValidationError


@transaction.atomic
def register_new_account(
    *,
    customer,
    season,
    name,
    notes="",
):
    account = Account.objects.create(
        customer=customer,
        season=season,
        name=name,
        notes=notes,
    )

    return account