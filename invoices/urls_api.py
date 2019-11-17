from django.urls import path
from . import views
# from django.contrib.auth.decorators import login_required
from django.conf.urls import include

from rest_framework import routers


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'currencys', views.CurrencyViewSet)
router.register(r'bank_accounts', views.BankAccountViewSet, base_name="bank_accounts")
router.register(r'bank_records', views.BankRecordViewSet, base_name="bank_records")
router.register(r'invoices_incoming', views.InvoicesIncomingViewSet, base_name="invoices_incoming")
router.register(r'invoices_outgoing', views.InvoicesOutgoingViewSet, base_name="invoices_outgoing")
router.register(r'invoices', views.InvoicesAllViewSet, base_name="invoices")
router.register(r'deals', views.DealViewSet, base_name="deals")


urlpatterns = [
    path('', include(router.urls)),
]
