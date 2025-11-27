from django import forms
from django.forms import widgets

from webapp.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]