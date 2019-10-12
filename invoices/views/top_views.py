from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from invoices.models import *
from invoices.forms import *


@login_required
def bank_records_index(request):
    context = {'test1': 'test1', 'test2': 'test2'}
    return render(request, "invoices/bank_records.html", context)

