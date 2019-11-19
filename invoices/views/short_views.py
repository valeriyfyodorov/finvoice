from django.views.generic import CreateView, UpdateView
from invoices.models import BankAccount, BankRecord
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

@method_decorator(user_passes_test(lambda u:u.is_staff), name='dispatch')
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
        if len(self.request.GET.get('returnUrl')) > 0:
            context['returnUrlHref'] = self.request.GET.get('returnUrl')
        else:
            context['returnUrlHref'] = self.returnUrlHref
        context['returnUrlText'] = "Return"
        return context

    def get_success_url(self, **kwargs):
        url = self.success_url
        if (len(self.request.POST.get('returnUrl')) > 0):
            url = self.request.POST.get('returnUrl')
        return url

@method_decorator(user_passes_test(lambda u:u.is_staff), name='dispatch')
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
        if len(self.request.GET.get('returnUrl')) > 0:
            context['returnUrlHref'] = self.request.GET.get('returnUrl')
        else:
            context['returnUrlHref'] = self.returnUrlHref
        context['returnUrlText'] = "Return"
        return context

    def get_success_url(self, **kwargs):
        url = self.success_url
        if (len(self.request.POST.get('returnUrl')) > 0):
            url = self.request.POST.get('returnUrl')
        return url

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
    
