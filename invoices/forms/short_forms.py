from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from invoices.models import BankAccount

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ('name', 'bank_name', 'bank_swift', 'account_name', 'payment_details', 'currency')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save account'))