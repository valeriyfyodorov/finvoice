from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'invoices'

urlpatterns = [
    # ex: /invoices/
    path('', login_required(views.index), name='index'),
    # ex: /invoices/5/
    path('bank_account/create/', views.BankAccountCreateView.as_view(), name='bank_account_create'),
    path('bank_account/update/<int:bank_account_id>/', views.BankAccountUpdateView.as_view(), name='bank_account_update'),
    path('bank_records', login_required(views.bank_records_index), name='bank_records_index'),
    path('<int:invoice_id>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('<int:invoice_id>/<int:use_stamp>/', views.InvoiceDetailView.as_view(), name='invoice_stamped_detail'),
    path('update/<int:invoice_id>/', views.InvoiceUpdate.as_view(), name='invoice_update'),
    path('delete/<int:invoice_id>/', views.InvoiceDelete.as_view(), name='invoice_delete'),
    path('create/', views.InvoiceCreate.as_view(), name='invoice_create'),
    # ex: /print/invoices/5/
    path('print/<int:invoice_id>/', views.print_detail, name='print_detail'),
    
]