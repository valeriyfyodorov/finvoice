from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from invoices.models import BankAccount, BankRecord, Invoice
from invoices.forms import BankAccountChoiceForm
import xml.etree.ElementTree as ET
from decimal import Decimal
from datetime import datetime
from django.contrib import messages
import re
from .helpers import set_invoice_deal_on_record_import

@login_required
def import_bank_statement(request):
    if request.method == 'POST':
        form = BankAccountChoiceForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
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
                    description = description.replace("maksājum", "")[:90]
                # print(name, recorded_date, amount, bank_ref, is_debit, description)
                bank_record = BankRecord.objects.create(name=name, 
                    bank_ref=bank_ref, recorded_date=recorded_date, 
                    description=description, amount=amount, bank_account=bank_account)
                set_invoice_deal_on_record_import(invoices_not_paid, bank_record)
            messages.success(request, 'File imported!')
        else:
            messages.error(request, 'Problem with form')
        return redirect('invoices:import_bank_statement')

    else:
        bank_records = BankRecord.objects.filter(deals=None)[:100]
        form = BankAccountChoiceForm
        context = {'bank_records': bank_records, 'form': form}
        return render(request, "invoices/import/bank_statement_import.html", context)
