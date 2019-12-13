from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from webparse.models import Symbol, QuoteIndication
from webparse.serializers import SymbolSerializer, QuoteIndicationSerializer
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework_datatables_editor.filters import DatatablesFilterBackend
# from rest_framework_datatables_editor.pagination import DatatablesPageNumberPagination
# from rest_framework_datatables_editor.renderers import DatatablesRenderer
from rest_framework_datatables_editor.viewsets import DatatablesEditorModelViewSet
# from rest_framework.response import Response
from datetime import datetime, timedelta, timezone
from webparse.views.helpers import raw_page_source


class SymbolViewSet(viewsets.ModelViewSet):
    queryset = Symbol.objects.all().order_by('name')
    serializer_class = SymbolSerializer


def get_quote_indication_options():
    return "options", {
        "symbol.id": [{'label': obj.ticket, 'value': obj.pk} for obj in Symbol.objects.all()],
    }


class QuoteIndicationsAllViewSet(DatatablesEditorModelViewSet):
    permission_classes = (DjangoModelPermissions, )
    serializer_class = QuoteIndicationSerializer
    queryset = QuoteIndication.objects

    def get_options(self):
        return get_quote_indication_options()

    def get_queryset(self):
        symbol_ticket = self.request.query_params.get('symbol_ticket', None)
        if symbol_ticket is not None:
            if len(symbol_ticket) == 0:
                symbol_ticket = None
            else:
                symbol_ticket = symbol_ticket.upper()
                indications = QuoteIndication.objects.filter(symbol__ticket=symbol_ticket)
                if indications:
                    indication = indications.latest('created_at', 'updated_at')
                    # print(datetime.now(timezone.utc), indication.updated_at, datetime.now(timezone.utc) - indication.updated_at)
                    if (datetime.now(timezone.utc) - indication.updated_at) > timedelta(hours=2):
                        raw_page_source(indication)
                        # print(indication.ticket)
            queryset = QuoteIndication.objects.all().filter(symbol__ticket=symbol_ticket)
        else:
            queryset = QuoteIndication.objects.all()
        return queryset

    class Meta:
        datatables_extra_json = ('get_options', )



