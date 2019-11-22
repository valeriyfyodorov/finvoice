import re

def set_invoice_deal_on_record_import(invoices_not_paid, bank_record, bank_deal):
    for invoice in invoices_not_paid:
        name = bank_record.name.lower().strip()
        if bank_deal and name == "bank":
            bank_record.deals.add(bank_deal)
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
        accept_for_deal = False
        mark_paid = False
        if (found_name or found_name_maybe) and found_number and found_amount:
            accept_for_invoice = True
            mark_paid = True
        elif (found_name or found_name_maybe) and found_number and (found_amount or found_advance):
            accept_for_invoice = True
        elif found_name and found_number and (invoice.total_gross < 0) and (bank_record.amount < 0):
            accept_for_invoice = True
        elif found_name and found_number and (invoice.total_gross > 0) and (bank_record.amount > 0):
            accept_for_deal = True
        if not accept_for_invoice and not accept_for_deal:
            continue
        if not accept_for_invoice and accept_for_deal:
            if invoice.deal:
                bank_record.deals.add(invoice.deal)
                bank_record.deal_related = True
                invoice.save()
                bank_record.save()
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
