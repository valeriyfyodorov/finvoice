from django.db import models
from django.core.validators import MaxLengthValidator
from .deal_models import Department

class GeneralSetting(models.Model):
    settingname = models.CharField(max_length=300)
    decimalvalue = models.DecimalField(default=0, max_digits=8, decimal_places=4)
    textvalue = models.CharField(max_length=300)
    
    class Meta:
        ordering = ('settingname',)

    def __str__(self):
        return self.settingname


class Company(models.Model):
    name = models.CharField(max_length=50)
    receiver_address = models.TextField(max_length=300, blank=True,
                                   validators=[MaxLengthValidator(300)])
    payment_address = models.TextField(max_length=300, blank=True,
                                   validators=[MaxLengthValidator(300)])
    country_code = models.TextField(max_length=3, blank=True,
                                   validators=[MaxLengthValidator(3)])
    eu_country = models.BooleanField(default=False)
    vat_number = models.CharField(max_length=30, blank=True, null=True,)
    
    invoiceNumberSignalString1 = models.CharField(max_length=50, blank=True, default='')
    invoiceNumberSignalString2 = models.CharField(max_length=50, blank=True, default='')
    invoiceNumberSkipCharacters = models.IntegerField(default=0)
    invoiceNumberStringLength = models.IntegerField(default=0)
    
    invoiceDateSignalString1 = models.CharField(max_length=50, blank=True, default='')
    invoiceDateSignalString2 = models.CharField(max_length=50, blank=True, default='')
    invoiceDateSkipCharacters = models.IntegerField(default=0)
    invoiceDateStringLength = models.IntegerField(default=0)
    invoiceDateStringFormat = models.CharField(max_length=20, blank=True, default='')

    invoiceAmountSignalString1 = models.CharField(max_length=50, blank=True, default='')
    invoiceAmountSignalString2 = models.CharField(max_length=50, blank=True, default='')
    invoiceAmountSkipCharacters = models.IntegerField(default=0)
    invoiceAmountStringLength = models.IntegerField(default=0)
    invoiceAmounCommaCharacter = models.CharField(max_length=3, blank=True, default='')
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


