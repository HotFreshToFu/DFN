from django import forms
from .models import Profile
from django.forms.widgets import DateInput


class ProfileForm(forms.ModelForm):
    WEX = forms.DateField(widget=forms.SelectDateWidget())
    DOB = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ('user',)
   