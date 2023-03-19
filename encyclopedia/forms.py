from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title", max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5}), label="Content")


