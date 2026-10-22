import requests

from django.conf import settings



class CollectionReminderService:

    @staticmethod
    def prepare(follow_up):
        payload = {
            "follow_up_id": follow_up.pk,
            "customer_name": follow_up.account.customer.name,
            "account_name": follow_up.account.name,
            "season": follow_up.account.season.name,
            "current_balance": str(follow_up.account.balance),
            "due_date": follow_up.due_date.isoformat(),
            "days_overdue": follow_up.days_overdue,
        }

        response = requests.post(
            settings.N8N_COLLECTION_REMINDER_WEBHOOK_URL,
            json = payload,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()
        reminder = data["reminder"]

        if not isinstance(reminder, str) or not reminder.strip():
            raise ValueError("n8n no ha devuelto un recordatorio válido.")

        return reminder