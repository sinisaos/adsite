from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"(?P<pk>\d+)/(?P<username>[\w-]+)/$",
        views.user_profile,
        name="profile",
    ),
    re_path(
        r"^(?P<pk>\d+)/update/(?P<username>[\w-]+)/$",
        views.update_profile,
        name="update-user",
    ),
    re_path(
        r"^(?P<pk>\d+)/delete-user/(?P<username>[\w-]+)/$",
        views.UserDeleteView.as_view(),
        name="delete-user",
    ),
]
