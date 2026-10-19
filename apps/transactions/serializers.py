from rest_framework import serializers

from apps.transactions.models import Transaction


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction

        fields = [
            "date",
            "description",
            "amount",
            "payment_method",
            "notes",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El importe debe ser mayor que cero."
            )

        return value

    def validate_payment_method(self, value):
        if not value:
            raise serializers.ValidationError(
                "Debes seleccionar un método de pago."
            )

        return value