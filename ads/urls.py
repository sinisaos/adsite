from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ad/(?P<slug>[\w-]+)/$', views.ad, name='ad'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit, name='edit'),
    url(r'^new/', login_required(views.AdView.as_view()), name="new"),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(views.AttachmentDeleteView.as_view()),
        name='upload_delete'),
    url(r'^ad-delete/(?P<pk>\d+)/$',
        login_required(views.AdDeleteView.as_view()), name='ad_delete'),
    url(r'^contact/(?P<slug>[\w-]+)/$', views.contact, name='contact'),
    url(r'^filter$', views.filter, name='filter'),
    url(r'^search$', views.search, name='search'),
]
