from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.db import transaction
from invoices.models import *
from invoices.forms import *
from datetime import date
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from django.http import HttpResponse
from django.template.loader import render_to_string


@login_required
def invoices_outgoing_index(request):
    if request.method == 'POST':
        form = TemplateChoiceForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data["template"])
            template = form.cleaned_data['template']
            first_jan = date(date.today().year, 1, 1)
            count_part = Invoice.objects.filter(issued_date__gte=first_jan).count()
            count_part += 1
            invoice = Invoice.objects.create_invoice_from_template(template, count_part)
            return redirect('invoices:invoice_update', invoice_id=invoice.pk)

    else:
        invoices = Invoice.objects.outgoing()[:150]
        form = TemplateChoiceForm
        context = {'invoices': invoices, 'form': form}
        return render(request, "invoices/index.html", context)


@login_required
def print_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    context = {
        'invoice': invoice,
        'title': "Invoice Rēķins "+str(invoice.number),
        'use_stamp': True,
    }
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "attachment; filename={name}-{number}-SHM.pdf".format(
        name="Invoice",
        number=invoice.number,
    )
    html = render_to_string('invoices/print_detail.html', context)
    font_config = FontConfiguration()
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config,)
    return response
    # return render(request, 'invoices/print_detail.html', context)


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'
    pk_url_kwarg = "invoice_id"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Invoice Rēķins " + context["invoice"].number
        context["use_stamp"] = self.kwargs.get('use_stamp', False)
        return context


class InvoiceCreate(LoginRequiredMixin, CreateView):
    model = Invoice
    template_name = 'invoices/invoice_create.html'
    form_class = InvoiceForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(InvoiceCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = InvoiceItemFormSet(self.request.POST)
        else:
            data['items'] = InvoiceItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            # form.instance.created_by = self.request.user
            self.object = form.save()
            if items.is_valid():
                items.instance = self.object
                items.save()
        return super(InvoiceCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('invoices:invoice_detail', kwargs={'invoice_id': self.object.pk})


class InvoiceUpdate(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_create.html'
    pk_url_kwarg = "invoice_id"

    def get_context_data(self, **kwargs):
        data = super(InvoiceUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = InvoiceItemFormSet(self.request.POST, instance=self.object)
        else:
            data['items'] = InvoiceItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if items.is_valid():
                items.instance = self.object
                items.save()
        return super(InvoiceUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('invoices:index')
        # return reverse_lazy('invoices:invoice_detail', kwargs={'invoice_id': self.object.pk})


class InvoiceDelete(LoginRequiredMixin, DeleteView):
    model = Invoice
    pk_url_kwarg = "invoice_id"
    template_name = 'invoices/confirm_delete.html'
    success_url = reverse_lazy('invoices:index')

