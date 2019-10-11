from rest_framework import viewsets
from invoices.models import Currency
from invoices.serializers import CurrencySerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all().order_by('name')
    serializer_class = CurrencySerializer
