from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from datetime import date
from invoices.models import BankAccount, BankRecord
from invoices.forms import BankAccountChoiceForm
import xml.etree.ElementTree as ET
from decimal import Decimal
from datetime import datetime
from django.contrib import messages


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
            for record in records:
                amount = Decimal(record.find('Amt').text)
                bank_ref = record.find('AcctSvcrRef').text
                if BankRecord.objects.filter(bank_ref=bank_ref):
                    continue # next record
                recorded_date = datetime.strptime(record.find('BookgDt').find('Dt').text, '%Y-%m-%d')
                is_debit = (record.find('CdtDbtInd').text == 'DBIT')
                details = record.find('NtryDtls').find('TxDtls')
                name = 'BANK'
                if len(details.find('RltdPties')) > 0:
                    if is_debit:
                        name = details.find('RltdPties').find('Cdtr').find('Nm').text[:12]
                    else:
                        name = details.find('RltdPties').find('Dbtr').find('Nm').text[:12]
                if is_debit: 
                    amount = -amount
                description = details.find('RmtInf').find('Ustrd')
                description = description.text.lower().replace("maksājumu uzdevuma ", "")
                description = description.replace("ārvalstu maksājumu ", "")
                description = description.replace("maksājum", "")[:20]
                # print(name, recorded_date, amount, bank_ref, is_debit, description)
                BankRecord.objects.create(name=name, bank_ref=bank_ref, recorded_date=recorded_date,
                    description=description, amount=amount, bank_account=bank_account)
            messages.success(request, 'File imported!')
        else:
            print("Not valid form")
        return redirect('invoices:import_bank_statement')

    else:
        bank_records = BankRecord.objects.filter(deals=None)[:100]
        form = BankAccountChoiceForm
        context = {'bank_records': bank_records, 'form': form}
        return render(request, "invoices/import/bank_statement_import.html", context)
