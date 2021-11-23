from django.contrib.auth.decorators import login_required
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^ad/(?P<slug>[\w-]+)/$", views.ad, name="ad"),
    re_path(r"^edit/(?P<pk>\d+)/$", views.edit, name="edit"),
    re_path(r"^new/", login_required(views.AdView.as_view()), name="new"),
    re_path(
        r"^delete/(?P<pk>\d+)/$",
        login_required(views.AttachmentDeleteView.as_view()),
        name="upload_delete",
    ),
    re_path(
        r"^ad-delete/(?P<pk>\d+)/$",
        login_required(views.AdDeleteView.as_view()),
        name="ad_delete",
    ),
    re_path(r"^contact/(?P<slug>[\w-]+)/$", views.contact, name="contact"),
    re_path(r"^filter$", views.filter, name="filter"),
    re_path(r"^search$", views.search, name="search"),
]
