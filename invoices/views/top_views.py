from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from invoices.models import *
from invoices.forms import *


@login_required
@user_passes_test(lambda u:u.is_staff)
def bank_records_index(request):
    masterTableURL = reverse_lazy('api:bank_accounts-list')
    childTableURL = reverse_lazy('api:bank_records-list')
    grandChildTableURL = reverse_lazy('api:invoices-list')
    context = {
        'master_header': 'Accounts', 
        'child_header': 'Records of account',
        'grand_child_header': 'Invoices for record',
        'default_is_incoming': '0',
        'childTableEmptyFilter': '0',
        'grandChildTableEmptyFilter': '0',
        'masterTableURL': masterTableURL,
        'childTableURL': childTableURL,
        'grandChildTableURL': grandChildTableURL,
        'returnUrl': reverse_lazy('invoices:bank_records_index'),
    }
    return render(request, "invoices/bank_records.html", context)


@login_required
def invoices_incoming_index(request):
    masterTableURL = reverse_lazy('api:invoices_incoming-list')
    childTableURL = reverse_lazy('api:bank_records-list')
    context = {
        'master_header': 'Invoices incoming', 
        'child_header': 'Bank records for invoice',
        'default_is_incoming': '1',
        'masterTableURL': masterTableURL,
        'childTableURL': childTableURL,
        'childTableEmptyFilter': '0',
        'masterTableFilterParameter': "id",
        'childTableFilterParameter': "invoice_selected",
        'returnUrl': reverse_lazy('invoices:invoices_incoming_index'),}
    return render(request, "invoices/invoices_to_bank_records.html", context)


@login_required
def invoices_outgoing_index(request):
    masterTableURL = reverse_lazy('api:invoices_outgoing-list')
    childTableURL = reverse_lazy('api:bank_records-list')
    context = {
        'master_header': 'Invoices outgoing', 
        'child_header': 'Bank records related to the deal',
        'default_is_incoming': '0',
        'masterTableURL': masterTableURL,
        'childTableURL': childTableURL,
        'childTableEmptyFilter': '0',
        'masterTableFilterParameter': "id",
        'childTableFilterParameter': "invoice_selected",
        'returnUrl': reverse_lazy('invoices:invoices_outgoing_index'),}
    return render(request, "invoices/invoices_to_bank_records.html", context)

@login_required
def invoices_unpaid_index(request):
    masterTableURL = reverse_lazy('api:invoices_unpaid-list')
    childTableURL = reverse_lazy('api:bank_records-list')
    context = {
        'master_header': 'Invoices unpaid', 
        'child_header': 'Bank records for invoice',
        'default_is_incoming': '0',
        'masterTableURL': masterTableURL,
        'childTableURL': childTableURL,
        'childTableEmptyFilter': "''",
        'masterTableFilterParameter': "deal.id",
        'childTableFilterParameter': "deal_selected",
        'returnUrl': reverse_lazy('invoices:invoices_unpaid_index'),}
    return render(request, "invoices/invoices_to_bank_records.html", context)

@login_required
def deals_index(request):
    grandMasterTableURL = reverse_lazy('api:deals-list')
    masterTableURL = reverse_lazy('api:invoices-list')
    childTableURL = reverse_lazy('api:bank_records-list')
    context = {
        'grand_master_header': 'Deals', 
        'master_header': 'Invoices related', 
        'child_header': 'Bank records related to deal',
        'default_is_incoming': '0',
        'grandMasterTableURL': grandMasterTableURL,
        'masterTableURL': masterTableURL,
        'childTableURL': childTableURL,
        'returnUrl': reverse_lazy('invoices:deals_index'),}
    return render(request, "invoices/deals_invoices_records.html", context)

