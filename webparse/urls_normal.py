from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'webparse'

urlpatterns = [
    # ex: /invoices/
    path('', views.test_index, name='test_index'),
    path('latest_quote/<str:prefix>', login_required(views.latest_quote), name='latest_quote'),
    path('future_quote/<str:prefix>', login_required(views.future_quote), name='future_quote'),
    path('quote_for_ticket/<str:ticket>', login_required(views.quote_for_ticket), name='quote_for_ticket'),
    # path('import_pdf_invoice', login_required(views.import_pdf_invoice), name='import_pdf_invoice'),
]