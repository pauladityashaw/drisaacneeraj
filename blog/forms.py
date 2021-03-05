from django import forms

class SearchForm(forms.Form):
    query = forms.CharField()

class EmailPostForm(forms.Form):
    email = forms.EmailField(label='Enter your email :', max_length=100, widget=forms.EmailInput(attrs={'class':'form-control'}))