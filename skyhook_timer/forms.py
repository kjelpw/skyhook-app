from django import forms
from skyhook_timer.models import SkyhookTimer

class SkyhookTimerForm(forms.ModelForm):
    days = forms.IntegerField(min_value=0, label="Days")
    hours = forms.IntegerField(min_value=0, max_value=23, label="Hours")
    minutes = forms.IntegerField(min_value=0, max_value=59, label="Minutes")
    class Meta:
        model = SkyhookTimer
        fields = ['eve_system', 'planet_number', 'countdown_time']
        widgets = {
            'countdown_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  # HTML5 input type for date-time picker
                'class': 'form-control',
            }),
        }
