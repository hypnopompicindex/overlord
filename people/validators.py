from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


def validate_monday(value):
    if (value.isoweekday() % 7) != 1:
        raise ValidationError('Date must be a Monday')
