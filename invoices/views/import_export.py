from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from invoices.models import BankAccount, BankRecord, Invoice, Deal, Template
from invoices.forms import BankAccountChoiceForm, CompanyChoiceForm
import xml.etree.ElementTree as ET
from decimal import Decimal
from datetime import datetime
from django.contrib import messages
import re
from .helpers import (
    set_invoice_deal_on_record_import, 
    mark_invoices_with_funds_enough_complete,
    new_incoming_invoice_object_from_pdf,
    invoice_already_exists
)

@login_required
def import_pdf_invoice(request):
    if request.method == 'POST':
        form = CompanyChoiceForm(request.POST, request.FILES)
        found_errors = False
        error_text = "Problem with form / file"
        if form.is_valid():
            company = None
            if (form.cleaned_data['company']):
                company = form.cleaned_data['company']
                deal = form.cleaned_data['deal']
            else:
                return redirect('invoices:import_pdf_invoice')
            files = request.FILES.getlist('files')
            # file = (request.FILES['file'])
            for file in files:
                invoice = new_incoming_invoice_object_from_pdf(company, file)
                if (invoice.total_gross != 0 and len(invoice.number) > 1):
                    if not invoice_already_exists(invoice):
                        invoice.deal = deal
                        invoice.save()
                    else:
                        found_errors = True
                        error_text = "Invoice already existed"
                else:
                    found_errors = True
                    error_text = "PDF file could not get all data"
        else:
            found_errors = True
            error_text = "Form not validated"
        if found_errors:
            messages.error(request, error_text)
        else:
            messages.success(request, 'File(s) imported')
        return redirect('invoices:invoices_incoming_index')

    else:
        form = CompanyChoiceForm
        context = {'form': form, "headingText": "Import invoice data from pdf"}
        return render(request, "invoices/import/company_selection_import.html", context)


@login_required
def import_bank_statement(request):
    if request.method == 'POST':
        form = BankAccountChoiceForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            bank_deal = Deal.objects.filter(name="BANK").first()
            internal_invoice = Invoice.objects.filter(number="INTERNAL").first()
            bank_account = None
            if (form.cleaned_data['bank_account']):
                bank_account = form.cleaned_data['bank_account']
            file = (request.FILES['file'])
            xml = ET.iterparse(file)
            for _, el in xml:
                prefix, has_namespace, postfix = el.tag.partition('}')
                if has_namespace:
                    el.tag = postfix  # strip all namespaces
            root = xml.root
            bank_account_name = root[0].find('Rpt').find('Acct').find('Id').find('IBAN').text
            if (not bank_account):
                bank_account = BankAccount.objects.filter(account_name=bank_account_name)[0]
            records = root[0].find('Rpt').findall('Ntry')
            invoices_not_paid = Invoice.objects.filter(is_paid=False)
            for record in records:
                amount = Decimal(record.find('Amt').text)
                bank_ref = record.find('AcctSvcrRef').text
                if BankRecord.objects.filter(bank_ref=bank_ref):
                    continue # next record
                recorded_date = datetime.strptime(record.find('BookgDt').find('Dt').text, '%Y-%m-%d').date()
                is_debit = (record.find('CdtDbtInd').text == 'DBIT')
                details = record.find('NtryDtls').find('TxDtls')
                name = 'BANK'
                if details.find('RltdPties') is not None and (len(details.find('RltdPties')) > 0):
                    if is_debit:
                        name = details.find('RltdPties').find('Cdtr').find('Nm').text
                    else:
                        name = details.find('RltdPties').find('Dbtr').find('Nm').text
                    name = re.sub('\d{4}\d+', '', name)
                    name = re.sub('\/', '', name)
                    name = re.sub('^\s*[\r\n]*\d+', '', name)[:40]
                if is_debit: 
                    amount = -amount
                description = ""
                if details.find('RmtInf') is not None:
                    description = details.find('RmtInf').find('Ustrd')
                    description = description.text.lower().replace("maksājumu uzdevuma ", "")
                    description = description.replace("ārvalstu maksājumu ", "")
                    description = re.sub('prepayment', '', description, flags=re.IGNORECASE)
                    description = description.replace("maksājum", "")[:100]
                # print(name, recorded_date, amount, bank_ref, is_debit, description)
                bank_record = BankRecord.objects.create(
                    name=name, 
                    bank_ref=bank_ref, recorded_date=recorded_date, 
                    description=description, amount=amount, bank_account=bank_account,
                    deal_related=False
                )
                set_invoice_deal_on_record_import(
                    invoices_not_paid, 
                    bank_record, 
                    bank_deal,
                    internal_invoice)
            messages.success(request, 'File imported!')
            mark_invoices_with_funds_enough_complete()
        else:
            messages.error(request, 'Problem with form')
        return redirect('invoices:import_bank_statement')

    else:
        bank_records = BankRecord.objects.filter(deals=None)[:100]
        form = BankAccountChoiceForm
        context = {'bank_records': bank_records, 'form': form}
        return render(request, "invoices/import/bank_statement_import.html", context)

