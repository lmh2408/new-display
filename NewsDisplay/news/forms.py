from django import forms
from .models import *

class ArticleUpload(forms.Form):
    section =  forms.ModelChoiceField(queryset=Section.objects.all(), to_field_name='section')
    author = forms.CharField(max_length=100)
    header = forms.CharField(max_length=200)
    subheader = forms.CharField(max_length=400)
    thumbnail = forms.ImageField()
    body = forms.CharField()


class ArticleEdit(forms.Form):
    author = forms.CharField(max_length=100)
    section = forms.ModelChoiceField(queryset=Section.objects.all(), to_field_name='section')
    header = forms.CharField(max_length=200)
    subheader = forms.CharField(max_length=400)
    thumbnail = forms.ImageField(required=False)
    body = forms.CharField()
