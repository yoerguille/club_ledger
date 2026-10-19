from django.db import transaction

from apps.collection.models import CollectionFollowUp
from apps.transactions.models import Transaction


@transaction.atomic
def register_payment(
    *,
    account,
    date,
    description,
    amount,
    payment_method,
    notes="",
):
    payment = Transaction.objects.create(
        account=account,
        movement_type=Transaction.MovementType.PAYMENT,
        date=date,
        description=description,
        amount=amount,
        payment_method=payment_method,
        notes=notes,
    )

    if account.balance <= 0:
        active_follow_up = account.active_collection_follow_up

        if active_follow_up:
            active_follow_up.status = CollectionFollowUp.Status.COMPLETED
            active_follow_up.save(update_fields=["status"])

    return payment