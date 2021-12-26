from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

import accounts.urls
import ads.urls
import profiles.urls
import questions.urls

from . import views

urlpatterns = [
    re_path(r"^$", views.HomePageView.as_view(), name="home"),
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^accounts/",
        include((accounts.urls, "accounts"), namespace="accounts"),
    ),
    re_path(
        r"^profile/",
        include((profiles.urls, "profiles"), namespace="profiles"),
    ),
    re_path(
        r"^questions/",
        include((questions.urls, "questions"), namespace="questions"),
    ),
    re_path(r"^messages/", include("django_messages.urls")),
    re_path(r"^ads/", include((ads.urls, "ads"), namespace="ads")),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
    re_path(
        r"^serviceworker.js",
        (
            TemplateView.as_view(
                template_name="serviceworker.js",
                content_type="application/javascript",
            )
        ),
        name="serviceworker.js",
    ),
    re_path(
        r"^manifest.json",
        (TemplateView.as_view(template_name="manifest.json")),
        name="manifest.json",
    ),
    re_path(r"^offline/", views.offline, name="offline"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
