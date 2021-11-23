from __future__ import unicode_literals

from authtools import forms as authtoolsforms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms
from django.contrib.auth import forms as authforms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError("A user with that email already exists.")
        return email


class PasswordChangeForm(authforms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field(
                "old_password",
                placeholder="Enter old password",
                css_class="form-control",
                autofocus="",
            ),
            Field(
                "new_password1",
                css_class="form-control",
                placeholder="Enter new password",
            ),
            Field(
                "new_password2",
                css_class="form-control",
                placeholder="Enter new password (again)",
            ),
            Submit(
                "pass_change",
                "Change Password",
                css_class="btn btn-lg btn-primary btn-block",
            ),
        )


class PasswordResetForm(authtoolsforms.FriendlyPasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("email", placeholder="Enter email", autofocus=""),
            Submit(
                "pass_reset",
                "Reset Password",
                css_class="btn btn-lg btn-primary btn-block",
            ),
        )


class SetPasswordForm(authforms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("new_password1", placeholder="Enter new password", autofocus=""),
            Field("new_password2", placeholder="Enter new password (again)"),
            Submit(
                "pass_change",
                "Change Password",
                css_class="btn btn-lg btn-primary btn-block",
            ),
        )
