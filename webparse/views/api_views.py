from rest_framework import viewsets
# from rest_framework.permissions import DjangoModelPermissions
from webparse.models import Symbol, QuoteIndication
from webparse.serializers import SymbolSerializer, QuoteIndicationSerializer
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework_datatables_editor.filters import DatatablesFilterBackend
# from rest_framework_datatables_editor.pagination import DatatablesPageNumberPagination
# from rest_framework_datatables_editor.renderers import DatatablesRenderer
from rest_framework_datatables_editor.viewsets import DatatablesEditorModelViewSet
# from rest_framework.response import Response
from webparse.views.helpers import update_or_create_indication, find_latest_ticket_for_commodity


class SymbolViewSet(viewsets.ModelViewSet):
    queryset = Symbol.objects.all().order_by('name')
    serializer_class = SymbolSerializer


def get_quote_indication_options():
    return "options", {
        "symbol.id": [{'label': obj.ticket, 'value': obj.pk} for obj in Symbol.objects.all()],
    }


class QuoteIndicationsAllViewSet(DatatablesEditorModelViewSet):
    serializer_class = QuoteIndicationSerializer
    queryset = QuoteIndication.objects

    def get_options(self):
        return get_quote_indication_options()

    def get_queryset(self):
        ticket = self.request.query_params.get('ticket', None)
        if ticket is not None:
            if len(ticket) == 0:
                ticket = None
            else:
                update_or_create_indication(ticket)
            queryset = QuoteIndication.objects.all().filter(symbol__ticket=ticket)
        else:
            queryset = QuoteIndication.objects.all()
        return queryset

    class Meta:
        datatables_extra_json = ('get_options', )

class CommodityIndicationLatestViewSet(DatatablesEditorModelViewSet):
    serializer_class = QuoteIndicationSerializer
    queryset = QuoteIndication.objects

    def get_options(self):
        return get_quote_indication_options()

    def get_queryset(self):
        prefix = self.request.query_params.get('prefix', None)
        if prefix is not None:
            if len(prefix) == 0:
                prefix = None
            else:
                ticket = find_latest_ticket_for_commodity(prefix)
                update_or_create_indication(ticket)
            queryset = QuoteIndication.objects.all().filter(symbol__ticket=ticket)[:1]
        else:
            queryset = QuoteIndication.objects.all()
        return queryset

    class Meta:
        datatables_extra_json = ('get_options', )

class CommodityIndicationFutureViewSet(DatatablesEditorModelViewSet):
    serializer_class = QuoteIndicationSerializer
    queryset = QuoteIndication.objects

    def get_options(self):
        return get_quote_indication_options()

    def get_queryset(self):
        prefix = self.request.query_params.get('prefix', None)
        if prefix is not None:
            if len(prefix) == 0:
                prefix = None
            else:
                ticket = find_latest_ticket_for_commodity(prefix, use_one_later=True)
                update_or_create_indication(ticket)
            queryset = QuoteIndication.objects.all().filter(symbol__ticket=ticket)[:1]
        else:
            queryset = QuoteIndication.objects.all()
        return queryset

    class Meta:
        datatables_extra_json = ('get_options', )





