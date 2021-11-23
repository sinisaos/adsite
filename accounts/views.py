from __future__ import unicode_literals

from authtools import views as authviews
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, FormView, UpdateView

from . import forms
from .forms import SignUpForm

User = get_user_model()


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=raw_password, email=email)
        login(self.request, user)
        subject = "Thank you for registering to our site"
        message = "Thank you for registering to our site, enjoy."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            email,
        ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect("/ads")


class UserDeleteView(DeleteView):
    model = User

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("home")


class UserEdit(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username"]
    template_name = "accounts/update.html"
    success_url = "/"


class PasswordChangeView(authviews.PasswordChangeView):
    form_class = forms.PasswordChangeForm
    template_name = "accounts/password-change.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your password was changed")
        return super(PasswordChangeView, self).form_valid(form)


class PasswordResetView(authviews.PasswordResetView):
    form_class = forms.PasswordResetForm
    template_name = "accounts/password-reset.html"
    success_url = reverse_lazy("accounts:password-reset-done")
    subject_template_name = "accounts/emails/password-reset-subject.txt"
    email_template_name = "accounts/emails/password-reset-email.html"


class PasswordResetDoneView(authviews.PasswordResetDoneView):
    template_name = "accounts/password-reset-done.html"


class PasswordResetConfirmView(authviews.PasswordResetConfirmAndLoginView):
    template_name = "accounts/password-reset-confirm.html"
    form_class = forms.SetPasswordForm
