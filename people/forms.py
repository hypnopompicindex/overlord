from django.forms import Form
from django import forms
from django.contrib.auth.models import User
from .models import Profile, TimeSheet
from django.forms import ModelForm
from django.forms import inlineformset_factory
from isoweek import Week
from datetime import datetime

w = Week(datetime.now().year, datetime.now().isocalendar()[1]).days()


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ()


class TimeSheetForm(ModelForm):
    class Meta:
        model = TimeSheet
        exclude = ()
        labels = {
            "monday": "Mon %s" % (w[0].strftime('%d %b'),),
            "tuesday": "Tue %s" % (w[1].strftime('%d %b'),),
            "wednesday": "Wed %s" % (w[2].strftime('%d %b'),),
            "thursday": "Thu %s" % (w[3].strftime('%d %b'),),
            "friday": "Fri %s" % (w[4].strftime('%d %b'),),
            "saturday": "Sat %s" % (w[5].strftime('%d %b'),),
            "sunday": "Sun %s" % (w[6].strftime('%d %b'),),
        }


TimeSheetFormSet = inlineformset_factory(User, TimeSheet, form=TimeSheetForm, extra=1)
#formset = TimeSheetFormSet(queryset=TimeSheet.objects.filter(week=1))
#TimeSheetQuery = TimeSheetFormSet(queryset=TimeSheet.objects.filter(week__exact=14))


class UserRegistrationForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('initials', 'mobile_phone', 'office_phone', 'date_of_birth', 'address', 'biography', 'notes', 'avatar')
