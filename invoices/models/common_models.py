from django.db import models
from django.core.validators import MaxLengthValidator

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
    eu_country = models.BooleanField(default=False)
    vat_number = models.CharField(max_length=30, blank=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


