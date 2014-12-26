from django import forms
from django.utils.html import escape

class TicketForm(forms.Form):
    title = forms.CharField()
    tags = forms.CharField(widget=forms.Textarea, required=False)
    raw_text = forms.CharField(widget=forms.Textarea, required=False)

    def clean_title(self):
        return escape(self.cleaned_data['title'])

    def clean_tags(self):
        if len(self.cleaned_data['tags']) == 0:
            return []
        tags = escape(self.cleaned_data['tags']).split()
        return [tag for tag in tags if len(tag) > 0]

    def clean_raw_text(self):
        return escape(self.cleaned_data['raw_text'])

class CommentForm(forms.Form):
    raw_text = forms.CharField(widget=forms.Textarea)

    def clean_raw_text(self):
        return escape(self.cleaned_data['raw_text'])
