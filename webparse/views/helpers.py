import requests
import html
from decimal import Decimal


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


def raw_page_source(indication):
    quoteCode = indication.symbol.ticket
    url = "https://www.barchart.com/futures/quotes/" + quoteCode + "/overview"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    r = requests.get(url, headers=headers)
    # print(r.encoding)
    raw_text = html.unescape(r.text)
    signal = "\"raw\":{\"lowPrice\":"
    look_from = raw_text.find(signal)
    price_low = valueFromSignal(raw_text, signal, look_from)
    if price_low > 0:
        indication.price_low = price_low
    # print(low_price_text)
    signal = "\"highPrice\":"
    price_high = valueFromSignal(raw_text, signal, look_from)
    if price_high > 0:
        indication.price_high = price_high
    # print(high_price_text)
    signal = "\"lastPrice\":"
    price_last = valueFromSignal(raw_text, signal, look_from)
    if price_last > 0:
        indication.price_last = price_last
    # print(last_price_text)
    signal = "\"previousPrice\":"
    price_previous = valueFromSignal(raw_text, signal, look_from)
    if price_previous > 0:
        indication.price_previous = price_previous
    # print(previous_price_text)
    indication.save()
    return indication


