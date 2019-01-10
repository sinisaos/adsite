from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'(?P<pk>\d+)/(?P<username>[\w-]+)/$', views.user_profile,
        name="profile"),
    url(r'^(?P<pk>\d+)/update/(?P<username>[\w-]+)/$',
        views.update_profile,
        name='update-user'),
    url(r'^(?P<pk>\d+)/delete-user/(?P<username>[\w-]+)/$',
        views.UserDeleteView.as_view(),
        name='delete-user')
]
