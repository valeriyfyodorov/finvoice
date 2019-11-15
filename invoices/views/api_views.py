from rest_framework import viewsets
from invoices.models import Currency, BankAccount, BankRecord, Invoice, Company, Deal
from invoices.serializers import CurrencySerializer, BankAccountSerializer, BankRecordSerializer, InvoiceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_datatables_editor.filters import DatatablesFilterBackend
from rest_framework_datatables_editor.pagination import DatatablesPageNumberPagination
from rest_framework_datatables_editor.renderers import DatatablesRenderer
from rest_framework_datatables_editor.viewsets import DatatablesEditorModelViewSet
from rest_framework.response import Response


class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all().order_by('name')
    serializer_class = BankAccountSerializer

def get_invoice_options():
    return "options", {
        "currency.id": [{'label': obj.name, 'value': obj.pk} for obj in Currency.objects.all()],
        "company.id": [{'label': obj.name, 'value': obj.pk} for obj in Company.objects.all()],
        "deal.id": [{'label': obj.name, 'value': obj.pk} for obj in Deal.objects.all()],
    }

class InvoicesIncomingViewSet(DatatablesEditorModelViewSet):
    queryset = Invoice.objects.incoming().order_by('-number')
    serializer_class = InvoiceSerializer

    def get_options(self):
        return get_invoice_options()

    class Meta:
        datatables_extra_json = ('get_options', )

class InvoicesOutgoingViewSet(DatatablesEditorModelViewSet):
    queryset = Invoice.objects.outgoing().order_by('-number')
    serializer_class = InvoiceSerializer

    def get_options(self):
        return get_invoice_options()

    class Meta:
        datatables_extra_json = ('get_options', )

class BankRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BankRecordSerializer

    def get_queryset(self):
        deal_selected = self.request.query_params.get('deal_selected', None)
        bank_account = self.request.query_params.get('bank_account', None)
        if bank_account is not None:
            queryset = BankRecord.objects.all().filter(bank_account=bank_account)
        else:
            queryset = BankRecord.objects.all()
        if deal_selected is not None:
            queryset = queryset.filter(deals__id=deal_selected)
        return queryset


# class CurrencyViewSet(viewsets.ModelViewSet):
#     queryset = Currency.objects.all().order_by('name')
#     serializer_class = CurrencySerializer

class CurrencyViewSet(viewsets.ViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    filter_backends = (DatatablesFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (DatatablesRenderer,)

    # def list(self, request):
    #     serializer = self.serializer_class(self.queryset, many=True)
    #     return Response(serializer.data)

    # def get_options(self):
    #     return get_invoice_options()

    # class Meta:
    #     datatables_extra_json = ('get_options', )

