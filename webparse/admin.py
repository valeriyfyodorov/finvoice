from django.contrib import admin
from .models import Symbol, QuoteIndication
# Register your models here.
class SymbolAdmin(admin.ModelAdmin):
    pass
admin.site.register(Symbol, SymbolAdmin)


class QuoteIndicationAdmin(admin.ModelAdmin):
    pass
admin.site.register(QuoteIndication, QuoteIndicationAdmin)
