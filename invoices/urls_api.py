from django.urls import path
from . import views
# from django.contrib.auth.decorators import login_required
from django.conf.urls import include

from rest_framework import routers


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'currencys', views.CurrencyViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
