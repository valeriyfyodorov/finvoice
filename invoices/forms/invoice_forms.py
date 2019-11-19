from django.forms import ModelForm, Textarea, Form, ModelChoiceField, HiddenInput, CharField
from flatpickr import DatePickerInput
from invoices.models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *

class Row(Div):
    css_class = "form-row"


class InvoiceItemForm(ModelForm):

    class Meta:
        model = InvoiceItem
        exclude = ()
        widgets = {
            'description': Textarea(attrs={'cols': 20, 'rows': 2}),
        }


InvoiceItemFormSet = inlineformset_factory(
    Invoice, InvoiceItem, form=InvoiceItemForm,
    fields=['order_number', 'description', 'price', 'quantity', 'total',], extra=1, can_delete=True
)


class InvoiceForm(ModelForm):
    returnUrl = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = Invoice
        exclude = []
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 1}),
            'payment_details': Textarea(attrs={'cols': 40, 'rows': 1}),
            'issued_date': DatePickerInput(
                options={
                    "dateFormat":"d/m/Y",
                }
            ),
            'payment_term': DatePickerInput(
                options={
                    "dateFormat":"d/m/Y",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-1 create-label'
        self.helper.field_class = 'col-md-1'
        self.helper.layout = Layout(
            Row(
                Field('number', wrapper_class='col-md-3'),
                Field('issued_date', wrapper_class='col-md-3'),
                Field('payment_term', wrapper_class='col-md-3'),
                Field('company', wrapper_class='col-md-3'),
            ),
            Row(
                Field('description', wrapper_class='col-md-3'),
                Div(css_class='col-md-3'),
                Field('currency', wrapper_class='col-md-3'),
                Field('is_incoming', wrapper_class='col-md-3'),
            ),
            Row(
                Field('total_net', wrapper_class='col-md-3'),
                Field('vat_percent', wrapper_class='col-md-3'),
                Field('total_vat', wrapper_class='col-md-3'),
                Field('total_gross', wrapper_class='col-md-3'),
                
            ),
            Row(
                Field('advance_required', wrapper_class='col-md-3'),
                Field('advance_percent', wrapper_class='col-md-3'),
                Field('advance_amount', wrapper_class='col-md-3'),
                Field('deal', wrapper_class='col-md-3'),
            ),
            Div(
                Fieldset('Add items',
                    Formset('items')),
            ),
            Row(
                ButtonHolder(Submit('submit', 'Save')),
                HTML("<br>"),
            ),
            HTML("<br>"),
            Row(
                HTML("<br>"),
                Field('is_paid', wrapper_class='col-md-3'),
                Field('payment_details', wrapper_class='col-md-3'),
                Field('returnUrl', wrapper_class='col-md-3'),
            )
        )
