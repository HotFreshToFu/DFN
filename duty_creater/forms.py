from django import forms
from django.forms import modelformset_factory
from .models import Event


class EventForm(forms.ModelForm):
    nurse = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly',}))
    date = forms.DateField(widget=forms.DateInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = Event
        # fields = ('duty',)
        fields = '__all__'

    # https://stackoverflow.com/questions/49640900/using-modelformset-factory-in-a-django-class-based-view
    # 우연히 찾은건데 form에서 검사를 하네 


# EventFormSet = modelformset_factory(Event, fields=('duty',))
EventFormSet = modelformset_factory(Event, form=EventForm, extra=0)