from django.contrib.auth import views as auth_views
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^login/$",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    re_path(
        r"^logout/$",
        auth_views.LogoutView.as_view(next_page="/ads"),
        name="logout",
    ),
    re_path(r"^signup/$", views.SignUpView.as_view(), name="signup"),
    re_path(
        r"^password-change/$",
        views.PasswordChangeView.as_view(),
        name="password-change",
    ),
    re_path(
        r"^password_reset/$",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    re_path(
        r"^password_reset/done/$",
        views.PasswordResetDoneView.as_view(),
        name="password-reset-done",
    ),
    re_path(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    re_path(
        r"^reset/done/$",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
