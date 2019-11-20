from django.db import models
from datetime import date
from django.core.validators import MaxLengthValidator
from django.db.models import Sum

class Department(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name


class Deal(models.Model):
    name = models.CharField(max_length=30, default="N/A D")
    started_date = models.DateField(default=date.today)
    department = models.ForeignKey(Department, related_name="deals", on_delete=models.CASCADE)

    @property
    def safe_name(self):
        return self.name or 'N/A D'

    class Meta:
        ordering = ('-started_date', 'name',)

    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=10)
    exchange_rate = models.DecimalField(default=1, max_digits=10, decimal_places=4)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class BankAccount(models.Model):
    name = models.CharField(max_length=30)
    bank_name = models.CharField(max_length=30)
    bank_swift = models.CharField(max_length=30)
    account_name = models.CharField(max_length=30)
    payment_details = models.TextField(max_length=300, blank=True,
                                   validators=[MaxLengthValidator(300)])
    currency = models.ForeignKey(Currency, related_name="accounts", on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ('bank_name','name',)

    def __str__(self):
        return self.name + '-' + self.currency.name

    def save(self, *args, **kwargs):
        balance = self.records.all().aggregate(Sum('amount'))['amount__sum']
        self.balance = balance
        super().save(*args, **kwargs)



