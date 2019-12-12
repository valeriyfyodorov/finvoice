from django.db import models
from django.core.validators import MaxLengthValidator
from decimal import Decimal

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
        return self.name


class QuoteIndication(models.Model):
    price_open = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_close = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_high = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_low = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    price_average = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    symbol = models.ForeignKey(Symbol, related_name="indications", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return self.quote.name + '-' + '{0:.2f}'.format(self.price_average)

    def save(self, *args, **kwargs):
        if self.price_close == 0:
            self.price_close = self.price_open
        self.price_average = round
        (
            (self.price_close + self.price_open + self.price_high) / Decimal(3.0),
            0
        )
        super().save(*args, **kwargs)
        self.symbol.save()

