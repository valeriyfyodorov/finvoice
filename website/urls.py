"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invoices/', include('invoices.urls_normal')),
    path('webparse/', include('webparse.urls_normal')),
    path(
        'accounts/login/', LoginView.as_view(
            template_name='admin/login.html',
            extra_context={
                'site_header': 'Restricted area',
            },
        )
    ),
    path('api/', include('invoices.urls_api')),
    path('json/', include('invoices.urls_json')),
    path('', include('frontside.urls_normal')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
