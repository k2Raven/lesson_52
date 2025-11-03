from django import forms
from django.forms import widgets

from webapp.models import status_choices

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=50, min_length=3, required=True, label='Название', widget=widgets.Input(attrs={'class': 'form-control'}))
    author = forms.CharField(max_length=50, required=True, label='Автор', widget=widgets.Input(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True, label='Контент')

    # status = forms.ChoiceField(choices=status_choices, label='Статус', widget=widgets.RadioSelect)
