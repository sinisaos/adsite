from django import forms
from django.forms import ModelForm, ValidationError
from multiupload.fields import MultiFileField
from .models import Ad, Attachment, Rent
import datetime


class AdForm(ModelForm):

    class Meta:
        model = Ad
        fields = ('category', 'title', 'brand', 'content', 'address', 'city',
                  'price', 'is_sold')

    files = MultiFileField(min_num=1, max_num=10,
                           max_file_size=1024 * 1024 * 5, required=False)

    def save(self, commit=True):
        instance = super(AdForm, self).save(commit)
        for each in self.cleaned_data['files']:
            Attachment.objects.create(file=each, ad=instance)
        return instance


class RentForm(ModelForm):
    ad_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Rent
        fields = ['ad_id', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super(RentForm, self).clean()
        ad = cleaned_data.get('ad_id')
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        between = Rent.objects.filter(
            ad=ad,
            start_date__lte=end,
            end_date__gte=start
        ).exclude(pk=self.instance.id)

        if start and end:
            now = datetime.datetime.now().date()
            diff = (now - start).total_seconds()
            if diff > 0:
                raise ValidationError("Both dates can't be in the past.")

            days = (end - start).days
            if days < 1:
                raise ValidationError("The minimum rental period is one day.")

            if any(between):
                raise ValidationError('Already rented in that time.')

        return cleaned_data
