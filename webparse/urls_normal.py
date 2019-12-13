from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'webparse'

urlpatterns = [
    # ex: /invoices/
    path('', views.test_index, name='test_index'),
    path('latest_quote/<str:ticket>', views.latest_quote, name='latest_quote'),
    # path('import_pdf_invoice', login_required(views.import_pdf_invoice), name='import_pdf_invoice'),
]