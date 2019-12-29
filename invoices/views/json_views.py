from rest_framework import viewsets
from invoices.models import Currency, BankAccount, BankRecord, Invoice
from invoices.serializers import CurrencySerializer, BankAccountSerializer, BankRecordSerializer, InvoiceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_datatables_editor.filters import DatatablesFilterBackend
from rest_framework_datatables_editor.pagination import DatatablesPageNumberPagination
from rest_framework_datatables_editor.renderers import DatatablesRenderer
from rest_framework_datatables_editor.viewsets import DatatablesEditorModelViewSet

from django.core import serializers
from django.http.response import JsonResponse


def currencyJsonList(request):
    return JsonResponse(list(Currency.objects.all().order_by('name').values()), safe=False)