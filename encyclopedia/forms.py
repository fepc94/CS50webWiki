from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 75%;'}))
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, 'class': 'form-control', 'style': 'width: 75%;'}), label="Content")

