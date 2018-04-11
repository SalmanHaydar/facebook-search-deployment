from django import forms
import datetime

class FormName(forms.Form):
    keyword = forms.CharField()
    # From = forms.DateField()
    # To = forms.DateField()
