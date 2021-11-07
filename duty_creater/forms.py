from django import forms
from django.forms import modelformset_factory
from .models import Event, ScheduleModification


class EventForm(forms.ModelForm):
    nurse = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly',}))
    date = forms.DateField(widget=forms.DateInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = Event
        fields = '__all__'

EventFormSet = modelformset_factory(Event, form=EventForm, extra=0)


class ScheduleModificationForm(forms.ModelForm):
    from_date = forms.DateField(label='휴무 시작일', widget=forms.SelectDateWidget())
    to_date = forms.DateField(label='휴무 종료일', widget=forms.SelectDateWidget())


    class Meta:
        model = ScheduleModification
        exclude = ('nurse', 'approval', )