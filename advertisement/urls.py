"""startapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
import accounts.urls
import profiles.urls
import questions.urls
import ads.urls
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(accounts.urls, namespace='accounts')),
    url(r'^profile/', include(profiles.urls, namespace='profiles')),
    url(r'^questions/', include(questions.urls, namespace='questions')),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^ads/', include(ads.urls, namespace='ads')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^serviceworker.js',
        (TemplateView.as_view(template_name="serviceworker.js",
                              content_type='application/javascript', )),
        name='serviceworker.js'),
    url(r'^manifest.json',
        (TemplateView.as_view(template_name="manifest.json")),
        name='manifest.json'),
    url(r'^offline/', views.offline, name='offline')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
