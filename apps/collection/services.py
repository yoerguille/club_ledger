from django.utils import timezone

from .models import CollectionFollowUp


def get_overdue_follow_ups():
    return (
        CollectionFollowUp.objects
        .filter(
            status=CollectionFollowUp.Status.ACTIVE,
            due_date__lt=timezone.localdate(),
        )
        .select_related(
            "account",
            "account__customer",
            "account__season",
        )
        .order_by("due_date")
    )