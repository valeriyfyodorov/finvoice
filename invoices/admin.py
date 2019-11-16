from django.contrib import admin
# Register your models here.
from .models import Invoice, InvoiceItem, GeneralSetting, Company, Template, TemplateItem
from .models import Deal, BankRecord, BankAccount, Department, Currency
from django.urls import reverse_lazy


admin.site.site_header = "Seahorse Management.  Settings"
admin.site.site_title = "Seahorse Management.  Settings"
admin.site.index_title = "Detailed settings"
admin.site.site_url = reverse_lazy('invoices:index')

class InvoiceItemsInline(admin.TabularInline):
    model = InvoiceItem

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        InvoiceItemsInline,
    ]
    list_display = ('number', 'company', 'issued_date', 
        'payment_term', 'description', 'currency', 'total_gross', 'is_paid',)
    readonly_fields = ["total_net", "total_gross", "total_vat"]
admin.site.register(Invoice, InvoiceAdmin)

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    readonly_fields = ('total',)
    editable_fields = []
    can_delete = False


class InvoiceItemAdmin(admin.ModelAdmin):
    readonly_fields = ['total',]
admin.site.register(InvoiceItem, InvoiceItemAdmin)


class TemplateItemsInline(admin.TabularInline):
    model = TemplateItem

class TemplateAdmin(admin.ModelAdmin):
    inlines = [
        TemplateItemsInline,
    ]
    list_display = ('company', 'description', 'currency', 'total_vat', 'total_gross', )
    readonly_fields = ["total_net", "total_gross", "total_vat"]
admin.site.register(Template, TemplateAdmin)

class TemplateItemInline(admin.TabularInline):
    model = TemplateItem
    readonly_fields = ('total',)
    editable_fields = []
    can_delete = False


class TemplateItemAdmin(admin.ModelAdmin):
    readonly_fields = ['total',]
admin.site.register(TemplateItem, TemplateItemAdmin)

class CompanyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Company, CompanyAdmin)

class GeneralSettingAdmin(admin.ModelAdmin):
    pass
admin.site.register(GeneralSetting, GeneralSettingAdmin)

class DealAdmin(admin.ModelAdmin):
    pass
admin.site.register(Deal, DealAdmin)

class BankRecordAdmin(admin.ModelAdmin):
    pass
admin.site.register(BankRecord, BankRecordAdmin)

class BankAccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(BankAccount, BankAccountAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Department, DepartmentAdmin)

class CurrencyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Currency, CurrencyAdmin)

