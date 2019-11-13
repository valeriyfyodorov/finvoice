from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'json'

urlpatterns = [
    # ex: /invoices/
    path('currency_list', login_required(views.currencyJsonList), name='currency_list'),
    
]