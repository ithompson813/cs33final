from django import forms

class NewGroupForm(forms.Form):
    name = forms.CharField(label="name", max_length="50")