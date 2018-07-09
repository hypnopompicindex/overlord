from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from workdays import workday
from workdays import networkdays
from datetime import datetime, timedelta

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
    initials = models.CharField(max_length=10, blank=True, null=True)
    mobile_phone = PhoneNumberField(blank=True, null=True)
    office_phone = PhoneNumberField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.user.username


class OutOfOffice(models.Model):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
#    number_of_days = models.PositiveIntegerField(null=True, blank=True)
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='out_of_office_person', blank=True, null=True)
    leave_type = models.CharField(choices=LEAVE_TYPE, max_length=200)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='out_of_office_project', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    approved = models.BooleanField()

    class Meta:
        verbose_name_plural = "Out of Office"
        verbose_name = "Out of Office"

    def __str__(self):
        if self.start_date is None:
            return 0
        else:
            return str(self.start_date)

    @property
    def number_of_days(self):
        holidays = [date(2018, 8, 6), date(2018, 9, 3), date(2018, 10, 8), date(2018, 12, 25), date(2018, 12, 26)]
        if self.start_date is None or self.end_date is None:
            return 0
        else:
            return networkdays(self.start_date, self.end_date + timedelta(days=-1), holidays=holidays)
