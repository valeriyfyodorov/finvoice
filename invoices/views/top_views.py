from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from invoices.models import *
from invoices.forms import *


@login_required
def bank_records_index(request):
    context = {'master_header': 'Accounts', 'child_header': 'Records'}
    return render(request, "invoices/bank_records.html", context)


@login_required
def invoices_incoming_index(request):
    context = {'master_header': 'Invoices incoming', 'child_header': 'Bank records for invoice'}
    return render(request, "invoices/invoices_incoming.html", context)

