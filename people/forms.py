from django.forms import Form
from django import forms
from django.contrib.auth.models import User
from .models import Profile, TimeSheet, Hours, TimeSheetWeek
from django.forms import ModelForm
from django.forms import inlineformset_factory
from isoweek import Week
from datetime import datetime
from projects.models import Project

w = Week(datetime.now().year, datetime.now().isocalendar()[1]).days()


class RequestKwargModelFormMixin(object):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # Pop the request off the passed in kwargs.
        super(RequestKwargModelFormMixin, self).__init__(*args, **kwargs)


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ()


class TimeSheetForm(RequestKwargModelFormMixin, ModelForm):
    class Meta:
        model = TimeSheet
        fields = ['project', 'week', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                  'saturday', 'sunday', 'approved', 'changes_required']
        labels = {
            "monday": "Mon %s" % (w[0].strftime('%d %b'),),
            "tuesday": "Tue %s" % (w[1].strftime('%d %b'),),
            "wednesday": "Wed %s" % (w[2].strftime('%d %b'),),
            "thursday": "Thu %s" % (w[3].strftime('%d %b'),),
            "friday": "Fri %s" % (w[4].strftime('%d %b'),),
            "saturday": "Sat %s" % (w[5].strftime('%d %b'),),
            "sunday": "Sun %s" % (w[6].strftime('%d %b'),),
        }
        widgets = {
            'week': forms.DateInput(attrs={'class':'weekPicker'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(TimeSheetForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.\
            filter(timesheets_closed=False).\
            filter(team_selection__exact=request.user.id)


#self.fields['project'].queryset = Project.objects.filter(timesheets_closed=False).filter(
#    team_selection__exact=self.instance)

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
        fields = ('initials', 'mobile_phone', 'office_phone', 'date_of_birth', 'address', 'biography', 'notes')


class HoursForm(RequestKwargModelFormMixin, ModelForm):
    class Meta:
        model = Hours
        fields = ['project', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                  'saturday', 'sunday']
        labels = {
            "monday": "Mon %s" % (w[0].strftime('%d %b'),),
            "tuesday": "Tue %s" % (w[1].strftime('%d %b'),),
            "wednesday": "Wed %s" % (w[2].strftime('%d %b'),),
            "thursday": "Thu %s" % (w[3].strftime('%d %b'),),
            "friday": "Fri %s" % (w[4].strftime('%d %b'),),
            "saturday": "Sat %s" % (w[5].strftime('%d %b'),),
            "sunday": "Sun %s" % (w[6].strftime('%d %b'),),
        }
        widgets = {
            'week': forms.DateInput(attrs={'class':'weekPicker'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(TimeSheet2Form, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.\
            filter(timesheets_closed=False).\
            filter(team_selection__exact=request.user.id)


HoursFormSet = inlineformset_factory(TimeSheetWeek, Hours, form=HoursForm, extra=1)
