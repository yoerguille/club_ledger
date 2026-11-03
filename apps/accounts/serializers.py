from apps.accounts.models import Account
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account

        fields = [
            "name",
            "notes",
        ]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "El nombre de la cuenta no puede estar vacío."
            )
        return value