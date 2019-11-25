from django.forms import Form, ModelChoiceField, FileField, ClearableFileInput
from invoices.models import Template, BankAccount, Company, Deal

class TemplateChoiceForm(Form):
    template = ModelChoiceField(queryset=Template.objects.all())

class CompanyChoiceForm(Form):
    company = ModelChoiceField(queryset=Company.objects.all())
    deal = ModelChoiceField(queryset=Deal.objects.all())
    files = FileField(widget=ClearableFileInput(attrs={'multiple': True}))
    # file = FileField()

class BankAccountChoiceForm(Form):
    bank_account = ModelChoiceField(queryset=BankAccount.objects.all())
    file = FileField()


