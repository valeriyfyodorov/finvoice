from rest_framework import serializers
from .models import Currency, BankAccount

class CurrencySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Currency
        fields = (
            'id', 'name', 'exchange_rate',
        )


class BankAccountSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    currency_name = serializers.ReadOnlyField(source='currency.name')
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = BankAccount
        fields = (
            'id', 'name', 'bank_name', 'bank_swift', 'account_name', 'payment_details', 'currency_name', 'currency',
        )
