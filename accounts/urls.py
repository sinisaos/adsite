from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login,
        {'template_name': 'accounts/login.html'}, name="login"),
    url(r'^logout/$', auth_views.logout,
        {'next_page': '/ads'}, name='logout'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^password-change/$', views.PasswordChangeView.as_view(),
        name='password-change'),
    url(r'^password_reset/$', views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(),
        name="password-reset-done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm"),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
    # url(r'^profile/$', views.UserProfile.as_view(),
    # name='profile'),
    # url(r'^profile/update/(?P<pk>\d+)/$', views.UserEdit.as_view(),
    #    name='update-user'),
    # url(r'^profile/delete_user/(?P<pk>\d+)/$',
    #    views.UserDeleteView.as_view(),
    #    name='delete-user'),
]
