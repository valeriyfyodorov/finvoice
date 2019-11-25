import textract
import datetime
from decimal import Decimal, InvalidOperation

import tempfile
import os


def invoice_dictionary_from_file(file, company):
    tempf, tempf_path = tempfile.mkstemp(suffix=".pdf")
    try:
        for chunk in file.chunks():
            os.write(tempf, chunk)
    except ValueError:
        raise Exception("Problem with the input file %s" % file.name)
    finally:
        os.close(tempf)
    page_content = textract.process(tempf_path, method='pdfminer')
    inner_text = page_content.decode("utf-8")
    # print(inner_text)
    invoiceNumber = inner_text[inner_text.find(company.invoiceNumberSignalString1):]
    invoiceNumberStartLocation = \
        invoiceNumber.find(company.invoiceNumberSignalString2) + \
        len(company.invoiceNumberSignalString2) + company.invoiceNumberSkipCharacters
    # print(invoiceNumber)
    invoiceNumber = (
        invoiceNumber[
            invoiceNumberStartLocation:
            invoiceNumberStartLocation + company.invoiceNumberStringLength
        ]
    ).strip().replace(u"\u00A0", "").replace(u"\u2028", "").replace(u"\u00AD", "-")
    # print("---" + invoiceNumber + "---")

    invoiceDate = inner_text[inner_text.find(company.invoiceNumberSignalString1):]
    invoiceDateStartLocation = \
        invoiceDate.find(company.invoiceDateSignalString2) + \
        len(company.invoiceDateSignalString2) + company.invoiceDateSkipCharacters
    # print(invoiceDate)
    invoiceDateStr = (
        invoiceDate[
            invoiceDateStartLocation:
            invoiceDateStartLocation + company.invoiceDateStringLength
        ]
    ).strip().replace(u"\u2028", "")
    try:
        invoiceDate = datetime.datetime.strptime(invoiceDateStr, company.invoiceDateStringFormat).date()
    except ValueError:
        invoiceDate = datetime.date.today()
    if invoiceDateStr == "":
        invoiceDate = datetime.date.today()
    # print("---" + invoiceDateStr + "---")
    # print(invoiceDate)
    invoiceAmount = inner_text[inner_text.find(company.invoiceAmountSignalString1):]
    invoiceAmountStartLocation = \
        invoiceAmount.find(company.invoiceAmountSignalString2) + \
        len(company.invoiceAmountSignalString2) + company.invoiceAmountSkipCharacters
    invoiceAmount = (
        invoiceAmount[
            invoiceAmountStartLocation:
            invoiceAmountStartLocation + company.invoiceAmountStringLength
        ]
    ).strip()
    invoiceAmount = invoiceAmount.replace(company.invoiceAmounCommaCharacter, '.')
    invoiceAmountStr = invoiceAmount.replace(' ', '')
    invoiceAmountStr = invoiceAmountStr.replace(u"\u00A0", "").replace(u"\u2028", "")
    try:
        invoiceAmount = Decimal(invoiceAmountStr)
    except InvalidOperation:
        invoiceAmount = 0

    # print("---" + invoiceAmountStr + "---")
    result = {'number': invoiceNumber, 'issued_date': invoiceDate, 'total_gross': invoiceAmount}
    # print(result)
    return result