from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Currency, BankAccount, BankRecord, Deal, Invoice, Company

class CurrencySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    # if we need to edit a field that is a nested serializer,
    # we must override to_internal_value method
    def to_internal_value(self, data):
        return get_object_or_404(Currency, pk=data['id'])

    class Meta:
        model = Currency
        fields = (
            'id', 'name', 'exchange_rate',
        )
        datatables_always_serialize = ('id',)


class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    def to_internal_value(self, data):
        return get_object_or_404(Company, pk=data['id'])

    class Meta:
        model = Company
        fields = (
            'id', 'name', 'vat_number',
        )
        datatables_always_serialize = ('id',)


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

    def to_internal_value(self, data):
        return get_object_or_404(Deal, pk=data['id'])
    
    class Meta:
        model = Deal
        fields = (
            'id', 'name', 'started_date', 'department', 'safe_name', 
        )
        datatables_always_serialize = ('id',)


class InvoiceSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    currency_name = serializers.ReadOnlyField(source='currency.name')
    company = CompanySerializer()
    company_name = serializers.ReadOnlyField(source='company.name')
    deal = DealSerializer(required=False)
    deal_name = serializers.ReadOnlyField(source='deal.name')
    DT_RowId = serializers.SerializerMethodField()
    DT_RowAttr = serializers.SerializerMethodField()
    # id = serializers.IntegerField(read_only=True)
    
    # currency_view = CurrencySerializer(source="currency", read_only=True)
    # bank_records = serializers.SerializerMethodField()

    # @staticmethod
    # def get_bank_records(invoice):
    #     return ', '.join([str(bank_record) for bank_record in invoice.bank_record.all()])

    @staticmethod
    def get_DT_RowId(invoice):
        return invoice.pk

    @staticmethod
    def get_DT_RowAttr(invoice):
        return {'data-pk': invoice.pk}
    
    class Meta:
        model = Invoice
        fields = (
            'DT_RowId', 'DT_RowAttr', 'number', 'issued_date', 'payment_term', 
            'company', 'company_name', 'total_net', 'total_gross', 
            'currency', 'currency_name', 'deal', 'deal_id', 'deal_name', 
            'is_incoming', 'vat_percent', 'is_paid', 
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
