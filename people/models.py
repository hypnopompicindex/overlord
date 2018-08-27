from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from workdays import workday
from workdays import networkdays
from datetime import datetime, timedelta
from django.urls import reverse
from .validators import validate_monday

LEAVE_TYPE = (
    ('VACATION', 'Vacation'),
    ('WFH', 'WFH'),
    ('LIEU TAKEN', 'Lieu Taken'),
    ('LIEU EARNED', 'Lieu Earned'),
    ('SICK', 'Sick'),
    ('EVENT', 'Event'),
)

USER_STATUS = (
    ('ACTIVE', 'Active'),
    ('ARCHIVE', 'Archive'),
    ('CONTRACT WORKER', 'Contract Worker'),
)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
#    user_status = models.CharField(choices=USER_STATUS, max_length=200)
#    initials = models.CharField(max_length=10, blank=True, null=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    home_phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_hire = models.DateField(blank=True, null=True)
    last_day_of_work = models.DateField(blank=True, null=True,
                                        help_text='*Only seen by Admin NEVER VISIBLE BY TEAM MEMBER')
    address = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField('Emergency Contact Name', blank=True, null=True, max_length=200)
    emergency_contact_mobile_phone = models.CharField('Emergency Contact Mobile Phone', blank=True, null=True, max_length=200)
    emergency_contact_home_phone = models.CharField('Emergency Contact Home Phone', blank=True, null=True, max_length=200)
    emergency_contact_address = models.TextField('Emergency Contact Address', blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def vacation_days(self):
        return User.objects.filter(outofoffice__leave_type__startswith="Vacation").annotate(Sum('outofoffice__number_of_days'))


class Holiday(models.Model):
    holiday_name = models.CharField(max_length=200)
    holiday_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['holiday_date']

    def __str__(self):
        return self.holiday_name


class OutOfOffice(models.Model):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    number_of_days = models.PositiveIntegerField(null=True, blank=True)
    person = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    leave_type = models.CharField(choices=LEAVE_TYPE, max_length=200)
#    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='out_of_office_project', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    submitted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    time_approved = models.DateTimeField(blank=True, null=True)
    by_whom = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Out of Office"
        verbose_name = "Out of Office"
        ordering = ('-start_date',)

    def __str__(self):
        if self.start_date is None:
            return 0
        else:
            return str(self.start_date)

    @property
    def name(self):
        return self.person.get_full_name()

    def save(self, *args, **kwargs):
        holidays = [date(2018, 8, 6), date(2018, 9, 3), date(2018, 10, 8), date(2018, 12, 25), date(2018, 12, 26)]
        if self.start_date is None or self.end_date is None:
            self.number_of_days = 0
        else:
            self.number_of_days = networkdays(self.start_date, self.end_date + timedelta(days=-1), holidays=holidays)
        super(OutOfOffice, self).save(*args, **kwargs)


class TimeSheet(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timesheet_person')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='timesheet')
    week = models.DateField(help_text='Must be a Monday', verbose_name='Start of Week', validators=[validate_monday])
    monday = models.CharField(max_length=20, blank=True, null=True, default=0)
    tuesday = models.CharField(max_length=20, blank=True, null=True, default=0)
    wednesday = models.CharField(max_length=20, blank=True, null=True, default=0)
    thursday = models.CharField(max_length=20, blank=True, null=True, default=0)
    friday = models.CharField(max_length=20, blank=True, null=True, default=0)
    saturday = models.CharField(max_length=20, blank=True, null=True, default=0)
    sunday = models.CharField(max_length=20, blank=True, null=True, default=0)
    hours = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    approved = models.BooleanField(default=False)
    changes_required = models.TextField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ('person', 'project', 'week')
        ordering = ('-week',)

    def __str__(self):
        return str(self.person)

    def get_absolute_url(self):
        return reverse('user-update', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.hours = float(self.monday) + float(self.tuesday) + float(self.wednesday) + \
                     float(self.thursday) + float(self.friday) + float(self.saturday) \
                     + float(self.sunday)
        super(TimeSheet, self).save(*args, **kwargs)

    @property
    def end_of_week(self):
        if self.week is None:
            return ' '
        else:
            return self.week + timedelta(days=6)


class TimeSheetWeek(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timesheetweek_person')
    week = models.DateField(help_text='Must be a Monday', verbose_name='Start of Week', validators=[validate_monday])
    changes_required = models.TextField(max_length=20, blank=True, null=True)
    approved = models.BooleanField(default=False)
    time_approved = models.DateTimeField(blank=True, null=True)
    by_whom = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('person', 'week')
        ordering = ('-week',)
        verbose_name = 'Timesheet'
        verbose_name_plural = 'Timesheets'

    def __str__(self):
        return 'Timesheet for {}, the week of {} to {}'.format(self.person, self.start_of_week, self.end_of_week)

    @property
    def start_of_week(self):
        if self.week is None:
            return ' '
        else:
            dt = self.week
            return dt.strftime("%b. %-d, %Y")

    @property
    def end_of_week(self):
        if self.week is None:
            return ' '
        else:
            dt = self.week + timedelta(days=6)
            return dt.strftime("%b. %-d, %Y")


class Hours(models.Model):
    time_sheet_week = models.ForeignKey(TimeSheetWeek, on_delete=models.CASCADE, related_name='time_sheet_weeks')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='timesheet2')
    monday = models.CharField(max_length=20, blank=True, null=True, default=0)
    tuesday = models.CharField(max_length=20, blank=True, null=True, default=0)
    wednesday = models.CharField(max_length=20, blank=True, null=True, default=0)
    thursday = models.CharField(max_length=20, blank=True, null=True, default=0)
    friday = models.CharField(max_length=20, blank=True, null=True, default=0)
    saturday = models.CharField(max_length=20, blank=True, null=True, default=0)
    sunday = models.CharField(max_length=20, blank=True, null=True, default=0)
    hours = models.DecimalField('Total Hours', null=True, blank=True, decimal_places=2, max_digits=10)

    class Meta:
        ordering = ('project',)
        verbose_name = 'Hours'
        verbose_name_plural = 'Hours'

    def __str__(self):
        return 'Timesheet on {} for the {} project'.format(self.time_sheet_week, self.project)

    def save(self, *args, **kwargs):
        self.hours = float(self.monday) + float(self.tuesday) + float(self.wednesday) + \
                     float(self.thursday) + float(self.friday) + float(self.saturday) \
                     + float(self.sunday)
        super(Hours, self).save(*args, **kwargs)

    @property
    def total_hours(self):
        return ",".join([str(p) for p in self.trim_set.all()])

    @property
    def total_cost(self):
        return self.hours * 40

