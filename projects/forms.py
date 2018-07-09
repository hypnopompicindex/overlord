from django import forms
from .models import Project
from django.forms import ModelForm, DateInput


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'event_start_date': forms.DateInput(attrs={'class':'datepicker'}),
        }