from django.urls import path
from . import views
# from django.contrib.auth.decorators import login_required
from django.conf.urls import include

from rest_framework import routers


app_name = 'webparseapi'

router = routers.DefaultRouter()
router.register(r'symbols', views.SymbolViewSet, base_name="symbols")
router.register(r'quotes', views.QuoteIndicationsAllViewSet, base_name="quotes")
router.register(r'latest', views.CommodityIndicationLatestViewSet, base_name="latest")
router.register(r'future', views.CommodityIndicationFutureViewSet, base_name="future")


urlpatterns = [
    path('', include(router.urls)),
]
