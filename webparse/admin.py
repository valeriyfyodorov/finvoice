from django.contrib import admin
from .models import Symbol, QuoteIndication, SymbolPeriod, SymbolCommodity
# Register your models here.
class SymbolAdmin(admin.ModelAdmin):
    pass
admin.site.register(Symbol, SymbolAdmin)

class QuoteIndicationAdmin(admin.ModelAdmin):
    pass
admin.site.register(QuoteIndication, QuoteIndicationAdmin)

class SymbolPeriodAdmin(admin.ModelAdmin):
    pass
admin.site.register(SymbolPeriod, SymbolPeriodAdmin)

class SymbolCommodityAdmin(admin.ModelAdmin):
    pass
admin.site.register(SymbolCommodity, SymbolCommodityAdmin)