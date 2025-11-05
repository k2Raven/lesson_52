from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets


def validate_author(value):
    if "@" in value:
        raise ValidationError('В имение автора не может быть данный символ "@"')


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=50, min_length=3, required=True, label='Название',
                            widget=widgets.Input(attrs={'class': 'form-control'}))
    author = forms.CharField(max_length=50, required=True, validators=[validate_author], label='Автор',
                             widget=widgets.Input(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True, label='Контент')

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if "*" in title:
            raise ValidationError('В название не может быть данный символ "*"')
        return title

    def clean(self):
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')
        if title and content and title == content:
            raise ValidationError('Название и контент не могут быть одинаковыми')
        return super().clean()
