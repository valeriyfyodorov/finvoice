from django.shortcuts import render
from webparse.models import *
from django.urls import reverse_lazy
from .helpers import raw_page_source
from datetime import datetime, timedelta, timezone

# Create your views here.
def test_index(request):
    indications = QuoteIndication.objects.all()[:150]
    context = {'indications': indications, 'returnUrl': reverse_lazy('webparse:test_index')}
    return render(request, "webparse/test_index.html", context)


def latest_quote(request, ticket):
    # print(ticket)
    ticket = ticket.upper()
    indication = QuoteIndication.objects.filter(symbol__ticket=ticket)
    if indication:
        indication = indication.latest('created_at', 'updated_at')
        # print(datetime.now(timezone.utc), indication.updated_at, datetime.now(timezone.utc) - indication.updated_at)
        if (datetime.now(timezone.utc) - indication.updated_at) > timedelta(hours=2):
            raw_page_source(indication)
            # print(indication.ticket)
    context = {'indication': indication, 'returnUrl': reverse_lazy('webparse:latest_quote')}
    return render(request, "webparse/latest_quote.html", context)


