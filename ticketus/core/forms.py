from django import forms
from django.utils.html import escape

class TicketForm(forms.Form):
    title = forms.CharField()
    raw_text = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        return escape(self.cleaned_data['title'])

    def clean_raw_text(self):
        return escape(self.cleaned_data['raw_text'])

class CommentForm(forms.Form):
    raw_text = forms.CharField(widget=forms.Textarea)

    def clean_raw_text(self):
        return escape(self.cleaned_data['raw_text'])
