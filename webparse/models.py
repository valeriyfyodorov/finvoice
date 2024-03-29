from django.db import models
from django.core.validators import MaxLengthValidator
from decimal import Decimal
from django.utils import timezone

class SymbolCommodity(models.Model):
    prefix = models.CharField(max_length=4)
    name = models.CharField(max_length=20)
    
    class Meta:
        ordering = ('prefix',)

    def __str__(self):
        return self.prefix

    def save(self, *args, **kwargs):
        self.prefix = self.prefix.upper()
        super().save(*args, **kwargs)

class SymbolPeriod(models.Model):
    suffix = models.CharField(max_length=4)
    name = models.CharField(max_length=20)
    valid_till = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ('suffix',)

    def __str__(self):
        return self.suffix

    def save(self, *args, **kwargs):
        self.suffix = self.suffix.upper()
        super().save(*args, **kwargs)

class Symbol(models.Model):
    ticket = models.CharField(max_length=10)
    name = models.CharField(
        max_length=200, 
        blank=True,
        validators=[MaxLengthValidator(200)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.ticket + ': ' + self.name

    def save(self, *args, **kwargs):
        if self.ticket:
            self.ticket = self.ticket.upper()
        super().save(*args, **kwargs)


class QuoteIndication(models.Model):
    price_open = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_close = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_low = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_high = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_last = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_previous = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_change = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_average = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    symbol = models.ForeignKey(Symbol, related_name="indications", on_delete=models.CASCADE)

    class Meta:
        ordering = ('-updated_at', '-created_at',)

    def __str__(self):
        return self.symbol.ticket + '-' + '{0:.2f}'.format(self.price_average)

    def save(self, *args, **kwargs):
        if self.price_open == 0:
            self.price_open = self.price_previous
        if self.price_open == 0:
            self.price_open = self.price_last
        if self.price_close == 0:
            self.price_close = self.price_previous
        if self.price_close == 0:
            self.price_close = self.price_open
        if self.price_previous > 0 and self.price_last > 0:
            self.price_change = self.price_last - self.price_previous
        self.price_average = round((self.price_close + self.price_open + self.price_last) / Decimal('3.0'), 0)
        # print(self.price_average)
        super().save(*args, **kwargs)
        self.symbol.save()

