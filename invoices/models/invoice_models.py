from django.db import models
from datetime import date, timedelta
from django.core.validators import MaxLengthValidator
from django.db.models import Sum
from decimal import Decimal
from .helpers import invoiceAutoNumber
from .common_models import Company
from .deal_models import Currency, Deal, BankAccount, Department

class InvoiceManager(models.Manager):
    def create_invoice_from_template(self, template, count_part, header=''):
        invoice = self.create(
            number=header + '' + invoiceAutoNumber(count_part),
            issued_date=date.today(),
            payment_term=date.today() + timedelta(days=7),
            company=template.company,
            description=template.description,
            total_net=template.total_net,
            vat_percent=template.vat_percent,
            total_gross=template.total_gross,
            advance_required=template.advance_required,
            advance_percent=template.advance_percent,
            advance_amount=template.advance_amount,
            is_paid=False,
            is_advance=template.is_advance,
            is_reissued=template.is_reissued,
            is_incoming=False,
            payment_details="",
            currency=template.currency,
        )
        for template_item in template.items.all():
            InvoiceItem.objects.create_invoice_item_from_template_item(template_item, invoice)
        return invoice

    def incoming(self):
        return self.get_queryset().filter(is_incoming=True).order_by('-issued_date', '-number')

    def compensated(self):
        return self.get_queryset().filter(is_reissued=True).filter(is_incoming=True).exclude(is_advance=True).order_by('company__name', '-number')

    def outgoing(self):
        return self.get_queryset().exclude(is_incoming=True).order_by('-issued_date', '-number')

    def charged(self):
        return self.get_queryset().exclude(is_incoming=True).exclude(is_advance=True).order_by('company__name', '-number')

    def unpaid(self):
        return self.get_queryset().exclude(is_paid=True).order_by('-issued_date', '-number')

    def financial(self):
        return self.get_queryset().exclude(is_advance=True).order_by('-issued_date', '-number')


class Invoice(models.Model):
    objects = InvoiceManager()
    number = models.CharField(max_length=20)
    issued_date = models.DateField(default=date.today)
    payment_term = models.DateField(default=date.today)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=True,
                                   validators=[MaxLengthValidator(300)])
    total_net = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    vat_percent = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    total_vat = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_gross = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_not_paid = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    advance_required = models.BooleanField(default=False)
    advance_percent = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    advance_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_to_pay = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    is_incoming = models.BooleanField(default=False)
    is_advance = models.BooleanField(default=False)
    is_reissued = models.BooleanField(default=True)
    is_credit = models.BooleanField(default=False)
    payment_details = models.TextField(max_length=100, blank=True,
                                   validators=[MaxLengthValidator(100)])
    currency = models.ForeignKey(Currency, related_name="invoices", on_delete=models.CASCADE, 
        null=False, blank=False, default=1) 
    deal = models.ForeignKey(Deal, related_name="invoices", on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='invoice_files/', blank=True)

    class Meta:
        ordering = ('-number', '-issued_date',)

    def __str__(self):
        return self.number

    def is_incoming_name(self):
        if self.is_incoming:
            return "INCM"
        else:
            return "OTGG" 

    def is_advance_name(self):
        if self.is_advance:
            return "ADVC"
        else:
            return "FNNN" 

    def file_size(self):
        try:
            return self.file.size
        except OSError:
            return 0
        except ValueError:
            return 0

    def save(self, *args, **kwargs):
        items_total_sum = self.items.all().aggregate(Sum('total'))['total__sum']
        if self.total_net == 0 or self.total_net is None:
            self.total_vat = round(
                self.total_gross * (
                    1 - (
                        Decimal('100.00') / (Decimal('100.00') + self.vat_percent)
                    )
                ), 2
            )
            self.total_net = round(self.total_gross - self.total_vat, 2)
        # print("STEP1", self.total_net, self.total_vat, self.total_gross)
        if self.is_incoming:
            self.total_net = -abs(self.total_net)
        elif items_total_sum is not None and items_total_sum != 0:
            self.total_net = items_total_sum
        elif not self.is_incoming:
            self.total_net = abs(self.total_net)
        self.total_net = round(self.total_net, 2)
        # print("STEP2", self.total_net, self.total_vat, self.total_gross)
        self.total_vat = self.total_net * self.vat_percent / Decimal('100.00')
        self.total_gross = round(self.total_net + self.total_vat, 2)
        if self.advance_required:
            self.advance_amount = self.total_gross * self.advance_percent / Decimal('100.00')
        else:
            self.advance_amount = 0
        bank_records_total_sum = 0
        if (self.id):
            bank_records_total_sum = self.bank_records.all().aggregate(Sum('amount'))['amount__sum'] or 0
            # print("Sum:" + bank_records_total_sum)
        # if bank_records_total_sum is None:
        #     bank_records_total_sum = 0
        if self.total_to_pay is None:
            self.total_to_pay = self.total_gross
        if not (self.id) and self.total_to_pay == 0:
            self.total_to_pay = self.total_gross
        self.total_not_paid = self.total_to_pay - bank_records_total_sum
        # print("STEP3", self.total_net, self.total_vat, self.total_gross)
        if self.is_credit:
            self.total_net = -self.total_net
            self.total_gross = -self.total_gross
        super().save(*args, **kwargs)


class InvoiceItemManager(models.Manager):
    def create_invoice_item_from_template_item(self, template_item, invoice):
        invoice_item = self.create(
            order_number=template_item.order_number,
            description=template_item.description,
            price=template_item.price,
            quantity=template_item.quantity,
            total=template_item.total,
            invoice=invoice,
        )
        return invoice_item


class InvoiceItem(models.Model):
    objects = InvoiceItemManager()
    order_number = models.IntegerField(default=1)
    description = models.CharField(max_length=200)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    quantity = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True)
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)

    class Meta:
        ordering = ('order_number',)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)
        self.invoice.save()

    def delete(self, *args, **kwargs):
        id = self.invoice.id
        super().delete(*args, **kwargs)
        invoice = Invoice.objects.get(id=id)
        invoice.save()


class Template(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=True,
                                   validators=[MaxLengthValidator(300)])
    total_net = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    vat_percent = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    total_vat = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_gross = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    advance_required = models.BooleanField(default=False)
    advance_percent = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    advance_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, related_name="templates", on_delete=models.CASCADE, 
        null=False, blank=False, default=1) 
    department = models.ForeignKey(Department, related_name="templates", on_delete=models.CASCADE, 
        null=False, blank=False, default=1)
    is_advance = models.BooleanField(default=False)
    is_reissued = models.BooleanField(default=True)

    class Meta:
        ordering = ('description',)

    def __str__(self):
        return self.currency.name + ' ' + self.department.name[:3] + '-' + self.description + '-' + self.company.name + self.currency.name

    def save(self, *args, **kwargs):
        items_total_sum = self.items.all().aggregate(Sum('total'))['total__sum']
        if items_total_sum:
            self.total_net = items_total_sum
        self.total_vat = self.total_net * self.vat_percent / Decimal('100.00')
        self.total_gross = self.total_net + self.total_vat
        if self.advance_required:
            self.advance_amount = self.total_gross * self.advance_percent / Decimal('100.00')
        super().save(*args, **kwargs)


class TemplateItem(models.Model):
    order_number = models.IntegerField(default=1)
    description = models.CharField(max_length=200)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    quantity = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True)
    template = models.ForeignKey(Template, related_name="items", on_delete=models.CASCADE)

    class Meta:
        ordering = ('order_number',)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)
        self.template.save()

    def delete(self, *args, **kwargs):
        id = self.template.id
        super().delete(*args, **kwargs)
        template = Template.objects.get(id=id)
        template.save()


class BankRecord(models.Model):
    name = models.CharField(max_length=40)
    bank_ref = models.CharField(max_length=30, default="", blank=True)
    recorded_date = models.DateField(default=date.today)
    description = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    used_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    bank_account = models.ForeignKey(BankAccount, related_name="records", on_delete=models.CASCADE)
    deal_related = models.BooleanField(default=True)
    deals = models.ManyToManyField(Deal, related_name="bank_records", blank=True)
    invoices = models.ManyToManyField(Invoice, related_name="bank_records", blank=True)

    class Meta:
        ordering = ('-recorded_date',)

    def __str__(self):
        return self.name + str(self.recorded_date)

    def save(self, *args, **kwargs):
        if (self.id and self.id > 0):
            self.deal_related = self.deals.exists()
        super().save(*args, **kwargs)
        self.bank_account.save()
