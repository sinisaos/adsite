from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Answer, Question


class QuestionForm(forms.ModelForm):
    details = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Question
        fields = ["qus", "details", "tags"]


class AnswerForm(forms.ModelForm):
    ans = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Answer
        fields = ["ans"]
