from django.forms import Form, ModelChoiceField, FileField
from invoices.models import Template, BankAccount

class TemplateChoiceForm(Form):
    template = ModelChoiceField(queryset=Template.objects.all())

class BankAccountChoiceForm(Form):
    bank_account = ModelChoiceField(queryset=BankAccount.objects.all())
    file = FileField()


