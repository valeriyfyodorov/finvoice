from dateutil import parser
from datetime import date
from django.db.models.functions import TruncDay
from django.db.models import Count


def invoiceAutoNumberForDate(date_selected, count_part):
    month_part = date_selected.strftime('%y%m')
    return month_part + str(count_part).zfill(3)


def invoiceAutoNumber(count_part):
    return invoiceAutoNumberForDate(date.today(), count_part)

