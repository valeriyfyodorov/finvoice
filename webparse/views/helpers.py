import requests
import html
from decimal import Decimal
from webparse.models import QuoteIndication, Symbol, SymbolPeriod, SymbolCommodity
from datetime import datetime, timedelta, timezone

def valueFromSignal(source, signal, look_from=0):
    start = source.find(signal, look_from)
    end = source.find(",", start)
    if start < 0 or end < 0:
        return "0"
    res_text = source[start + len(signal):end]
    try:
        dec = Decimal(res_text)
        return dec
    except:
        return 0

class IndicatorQuoteSet:
    def __init__(self):
        self.ticket = None
        self.price_open = 0
        self.price_close = 0
        self.price_low = 0
        self.price_high = 0
        self.price_last = 0
        self.price_previous = 0
        self.price_change = 0

def get_quotset_from_barchart(ticket):
    quoteSet = IndicatorQuoteSet()
    url = "https://www.barchart.com/futures/quotes/" + ticket + "/overview"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    r = requests.get(url, headers=headers)
    # print(r.encoding)
    raw_text = html.unescape(r.text)
    signal = "\"raw\":{\"lowPrice\":"
    look_from = raw_text.find(signal)
    if look_from < 0:
        return quoteSet
    quoteSet.ticket = ticket
    quoteSet.price_low = valueFromSignal(raw_text, signal, look_from)
    signal = "\"openPrice\":"
    quoteSet.price_open = valueFromSignal(raw_text, signal, look_from)
    signal = "\"highPrice\":"
    quoteSet.price_high = valueFromSignal(raw_text, signal, look_from)
    # print(high_price_text)
    signal = "\"lastPrice\":"
    quoteSet.price_last = valueFromSignal(raw_text, signal, look_from)
    # print(last_price_text)
    signal = "\"previousPrice\":"
    quoteSet.price_previous = valueFromSignal(raw_text, signal, look_from)
    return quoteSet

def quoteset_to_indication(quoteSet, indication):
    indication.price_open = quoteSet.price_open
    indication.price_close = quoteSet.price_close
    indication.price_low = quoteSet.price_low
    indication.price_high = quoteSet.price_high
    indication.price_last = quoteSet.price_last
    indication.price_previous = quoteSet.price_previous
    indication.price_change = quoteSet.price_change

def indication_from_barchart_and_save(indication, ticket):
    quoteSet = get_quotset_from_barchart(ticket)
    if quoteSet.ticket:
        quoteset_to_indication(quoteSet, indication)
        indication.save()

def update_or_create_indication(ticket, minutes_ignore=120):
    ticket = ticket.strip()
    if len(ticket) < 5:
        return None
    ticket = ticket.upper()
    indication = QuoteIndication.objects.filter(symbol__ticket=ticket)
    if indication:
        indication = indication.latest('created_at', 'updated_at')
        # print(datetime.now(timezone.utc), indication.updated_at, datetime.now(timezone.utc) - indication.updated_at)
        if (datetime.now(timezone.utc) - indication.updated_at) > timedelta(minutes=minutes_ignore):
            indication_from_barchart_and_save(indication, ticket)
    else:
        symbol = Symbol.objects.filter(ticket=ticket).first()
        if symbol: # has this symbol, not yet records for it
            indication = QuoteIndication(symbol=symbol)
            indication_from_barchart_and_save(indication, ticket)
        else: # not even symbol for this ticket
            suffix = ticket[-3:]
            prefix = ticket[:2]
            commodity = SymbolCommodity.objects.filter(prefix=prefix).first()
            period = SymbolPeriod.objects.filter(suffix=suffix).first()
            if commodity and period:
                symbol = Symbol.objects.create(ticket=ticket, name=(commodity.name + ' ' + period.name))
                indication = QuoteIndication(symbol=symbol)
                indication_from_barchart_and_save(indication, ticket)
    return indication

def find_latest_ticket_for_commodity(prefix, use_one_later=False):
    prefix = prefix.upper()
    period = SymbolPeriod.objects.order_by('valid_till').filter(valid_till__gt=datetime.now(timezone.utc)).first()
    if not period:
        return ""
    if use_one_later:
        period = SymbolPeriod.objects.order_by('valid_till').filter(valid_till__gt=period.valid_till).first()
    if not period:
        return ""
    commodity = SymbolCommodity.objects.filter(prefix=prefix).first()
    if not commodity:
        return ""
    return commodity.prefix + period.suffix
