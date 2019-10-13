from django.views.generic import CreateView, UpdateView
from invoices.models import BankAccount, BankRecord
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class ShortCreateView(LoginRequiredMixin, CreateView):
    fields = '__all__'
    template_name = "invoices/short_forms/create.html"
    success_url = reverse_lazy('invoices:index')
    modelDescriptiveName = "modelName"
    returnUrlHref = reverse_lazy('invoices:index')

    def get_context_data(self, **kwargs):
        context = super(ShortCreateView, self).get_context_data(**kwargs)
        context['headerText'] = "Add new " + self.modelDescriptiveName
        context['submitText'] = "Create new " + self.modelDescriptiveName
        context['returnUrlHref'] = self.returnUrlHref
        context['returnUrlText'] = "Return"
        return context

class ShortUpdateView(LoginRequiredMixin, UpdateView):
    fields = '__all__'
    template_name = "invoices/short_forms/create.html"
    success_url = reverse_lazy('invoices:index')
    modelDescriptiveName = "modelName"
    returnUrlHref = reverse_lazy('invoices:index')

    def get_context_data(self, **kwargs):
        context = super(ShortUpdateView, self).get_context_data(**kwargs)
        context['headerText'] = "Update " + self.modelDescriptiveName
        context['submitText'] = "Save " + self.modelDescriptiveName
        context['returnUrlHref'] = self.returnUrlHref
        context['returnUrlText'] = "Return"
        return context

class BankAccountCreateView(ShortCreateView):
    model = BankAccount
    modelDescriptiveName = "account"
    success_url = reverse_lazy('invoices:bank_records_index')

class BankAccountUpdateView(ShortUpdateView):
    model = BankAccount
    modelDescriptiveName = "account"
    success_url = reverse_lazy('invoices:bank_records_index')
    pk_url_kwarg = "bank_account_id"
    
class BankRecordCreateView(ShortCreateView):
    model = BankRecord
    modelDescriptiveName = "record"
    success_url = reverse_lazy('invoices:bank_records_index')

class BankRecordUpdateView(ShortUpdateView):
    model = BankRecord
    modelDescriptiveName = "record"
    success_url = reverse_lazy('invoices:bank_records_index')
    pk_url_kwarg = "bank_record_id"
    
