from apps.accounts.models import Account
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account

        fields = [
            "season",
            "name",
            "notes",
        ]

    def validate_season(self, value):
        if not value:
            raise serializers.ValidationError(
                "Debes seleccionar una temporada."
            )

        return value
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "El nombre de la cuenta no puede estar vacío."
            )
        return value