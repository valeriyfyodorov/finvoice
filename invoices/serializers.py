from rest_framework import serializers
from .models import Currency, BankAccount, BankRecord, Deal, Invoice, Company

class CurrencySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Currency
        fields = (
            'id', 'name', 'exchange_rate',
        )

class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = (
            'id', 'name', 'vat_number',
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

class DealSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Deal
        fields = (
            'id', 'name', 'started_date', 'department', 'safe_name', 
        )

class InvoiceSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    currency_name = serializers.ReadOnlyField(source='currency.name')
    company = CompanySerializer()
    company_name = serializers.ReadOnlyField(source='company.name')
    # deal_name = serializers.ReadOnlyField(source='deal.safe_name', default="N/A D")
    # deal = serializers.ReadOnlyField(source='deal.id', default=0)
    deal = DealSerializer(required=False)
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Invoice
        fields = (
            'id', 'number', 'issued_date', 'payment_term', 
            'company', 'company_name', 'total_net', 'total_gross', 
            'currency', 'currency_name', 'deal', 'deal_id',
        )

class BankRecordSerializer(serializers.ModelSerializer):
    bank_account = BankAccountSerializer()
    deals = serializers.SerializerMethodField()

    def get_deals(self, bank_account):
        return ', '.join([str(deal) for deal in bank_account.deals.all()])

    bank_account_name = serializers.ReadOnlyField(source='bank_account.name')
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = BankRecord
        fields = (
            'id', 'recorded_date', 'description', 'amount', 
            'used_amount', 'deal_related', 'deals', 'bank_account', 'bank_account_name',
        )
