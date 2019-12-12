from django.shortcuts import render
from webparse.models import *
from django.urls import reverse_lazy
from .helpers import raw_page_source

# Create your views here.
def test_index(request):
    indications = QuoteIndication.objects.all()[:150]
    context = {'indications': indications, 'returnUrl': reverse_lazy('webparse:test_index')}
    return render(request, "webparse/test_index.html", context)

