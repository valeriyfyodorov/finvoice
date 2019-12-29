from django.shortcuts import render
from webparse.models import *
from django.urls import reverse_lazy
from .helpers import update_or_create_indication, find_latest_ticket_for_commodity

# Create your views here.
def test_index(request):
    indications = QuoteIndication.objects.all()[:150]
    context = {'indications': indications, 'returnUrl': reverse_lazy('webparse:test_index')}
    return render(request, "webparse/test_index.html", context)


def quote_for_ticket(request, ticket):
    indication = update_or_create_indication(ticket)
    context = {'indication': indication, 'returnUrl': reverse_lazy('webparse:latest_quote')}
    return render(request, "webparse/latest_quote.html", context)


def latest_quote(request, prefix):
    ticket = find_latest_ticket_for_commodity(prefix=prefix, use_one_later=False)
    indication = update_or_create_indication(ticket)
    context = {'indication': indication, 'returnUrl': reverse_lazy('webparse:latest_quote')}
    return render(request, "webparse/latest_quote.html", context)

def future_quote(request, prefix):
    ticket = find_latest_ticket_for_commodity(prefix=prefix, use_one_later=True)
    indication = update_or_create_indication(ticket)
    context = {'indication': indication, 'returnUrl': reverse_lazy('webparse:latest_quote')}
    return render(request, "webparse/latest_quote.html", context)



