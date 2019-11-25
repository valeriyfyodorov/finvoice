import re
from invoices.models import BankRecord, Invoice
from django.db.models import Sum
import datetime
from .import_misc.pdf_import import invoice_dictionary_from_file


def invoice_already_exists(invoice):
    total_gross = -abs(invoice.total_gross)
    invoices_available = Invoice.objects.filter(
        is_incoming=invoice.is_incoming, 
        company=invoice.company,
        number=invoice.number,
        issued_date=invoice.issued_date, 
        total_gross=total_gross
    )
    print(invoices_available)
    invoices_available_count = invoices_available.count()
    print("count: ", invoices_available_count)
    return invoices_available_count > 0


def new_incoming_invoice_object_from_pdf(company, file):
    parsed_invoice = invoice_dictionary_from_file(file, company)
    invoice = Invoice(
        number=parsed_invoice['number'],
        issued_date=parsed_invoice['issued_date'],
        total_gross=parsed_invoice['total_gross'],
        is_incoming=True,
        company=company,
        vat_percent=0,
        advance_required=False,
    )
    return invoice

def mark_invoices_with_funds_enough_complete():
    invoices_not_paid = Invoice.objects.filter(is_paid=False)
    for invoice in invoices_not_paid:
        if not invoice.deal or invoice.is_paid:
            continue
        bank_records_for_deal = BankRecord.objects \
            .filter(deals=invoice.deal).filter(name__icontains=invoice.company.name)
        if not bank_records_for_deal:
            continue
        invoices_for_deal = Invoice.objects \
            .filter(company=invoice.company).filter(deal=invoice.deal)
        sum_of_paid_for_company = bank_records_for_deal.aggregate(Sum('amount'))['amount__sum']
        sum_of_invoices_for_company = invoices_for_deal.aggregate(Sum('total_gross'))['total_gross__sum']
        if sum_of_invoices_for_company == sum_of_paid_for_company:
            invoices_for_deal.update(is_paid=True)    


def set_invoice_deal_on_record_import(invoices_not_paid, bank_record, bank_deal, internal_invoice):
    for invoice in invoices_not_paid:
        name = bank_record.name.lower().strip()
        if bank_deal and name == "bank":
            bank_record.deals.add(bank_deal)
            if internal_invoice:
                bank_record.invoices.add(internal_invoice)
            bank_record.deal_related = True
            bank_record.save()
            continue
        if len(bank_record.description) < 3 and name != "bank":
            continue
        if invoice.currency != bank_record.bank_account.currency:
            continue
        if invoice.issued_date > bank_record.recorded_date:
            continue
        description = bank_record.description.lower()
        modified_number = re.sub('^[^0-9]+[\s\-]?', '', invoice.number)
        found_number = modified_number.lower().strip() in description
        found_name_maybe = invoice.company.name.lower().strip()[:10].strip() in name
        found_name = invoice.company.name.lower().strip() in name
        found_amount = (invoice.total_gross == bank_record.amount)
        found_advance = (invoice.advance_amount == bank_record.amount)
        accept_for_invoice = False
        mark_paid = False
        if (found_name or found_name_maybe) and found_number and found_amount:
            accept_for_invoice = True
            mark_paid = True
        elif (found_name or found_name_maybe) and found_number and (found_amount or found_advance):
            accept_for_invoice = True
        elif found_name and found_number and (invoice.total_gross < 0) and (bank_record.amount < 0):
            accept_for_invoice = True
        elif found_name and found_number and (invoice.total_gross > 0) and (bank_record.amount > 0):
            accept_for_invoice = True
        if not accept_for_invoice:
            continue
        # some valuable info says bank record belongs to the invoice
        invoice.bank_records.add(bank_record)
        if mark_paid:
            invoice.is_paid = True
        invoice.save()
        if invoice.deal:
            bank_record.deals.add(invoice.deal)
        bank_record.deal_related = True
        bank_record.save()
