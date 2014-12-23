from django import forms
from django.utils.html import escape

class CommentForm(forms.Form):
    raw_text = forms.CharField(widget=forms.Textarea)

    def clean_raw_text(self):
        return escape(self.cleaned_data['raw_text'])
