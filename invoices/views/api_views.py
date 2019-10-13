from rest_framework import viewsets
from invoices.models import Currency, BankAccount, BankRecord
from invoices.serializers import CurrencySerializer, BankAccountSerializer, BankRecordSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_datatables.filters import DatatablesFilterBackend

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all().order_by('name')
    serializer_class = CurrencySerializer

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all().order_by('name')
    serializer_class = BankAccountSerializer

# class BankRecordViewSet(viewsets.ModelViewSet):
#     queryset = BankRecord.objects.all().order_by('name')
#     serializer_class = BankRecordSerializer
#     filter_backends = [DatatablesFilterBackend]
#     filterset_fields = (
#         'bank_account',
#     )

class BankRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BankRecordSerializer

    def get_queryset(self):
        bank_account = self.request.query_params.get('bank_account', None)
        if bank_account is not None:
            queryset = BankRecord.objects.all().filter(bank_account=bank_account)
        else:
            queryset = BankRecord.objects.all()
        return queryset

