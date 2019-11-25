from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'invoices'

urlpatterns = [
    # ex: /invoices/
    path('', login_required(views.invoices_creation_index), name='index'),
    path('invoices_incoming', login_required(views.invoices_incoming_index), name='invoices_incoming_index'),
    path('invoices_outgoing', login_required(views.invoices_outgoing_index), name='invoices_outgoing_index'),
    path('invoices_unpaid', login_required(views.invoices_unpaid_index), name='invoices_unpaid_index'),
    path('deals', login_required(views.deals_index), name='deals_index'),
    path('companies_accounts', login_required(views.companies_accounts), name='companies_accounts'),
    path('bank_account/create/', views.BankAccountCreateView.as_view(), name='bank_account_create'),
    path('bank_account/update/<int:bank_account_id>/', views.BankAccountUpdateView.as_view(), name='bank_account_update'),
    path('bank_record/create/', views.BankRecordCreateView.as_view(), name='bank_record_create'),
    path('bank_record/update/<int:bank_record_id>/', views.BankRecordUpdateView.as_view(), name='bank_record_update'),
    path('bank_records', login_required(views.bank_records_index), name='bank_records_index'),
    path('statement_import', login_required(views.import_bank_statement), name='import_bank_statement'),
    path('import_pdf_invoice', login_required(views.import_pdf_invoice), name='import_pdf_invoice'),
    path('<int:invoice_id>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('<int:invoice_id>/<int:use_stamp>/', views.InvoiceDetailView.as_view(), name='invoice_stamped_detail'),
    path('update/<int:invoice_id>/', views.InvoiceUpdate.as_view(), name='invoice_update'),
    path('delete/<int:invoice_id>/', views.InvoiceDelete.as_view(), name='invoice_delete'),
    path('create/', views.InvoiceCreate.as_view(), name='invoice_create'),
    # ex: /print/invoices/5/
    path('print/<int:invoice_id>/', views.print_detail, name='print_detail'),
    
]