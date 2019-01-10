from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    image = forms.FileField(required=False)

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'image')
