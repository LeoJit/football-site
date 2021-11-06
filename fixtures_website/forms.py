from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(max_length=100, widget= forms.TextInput(attrs={"class" : 'form-control'}), required = True)