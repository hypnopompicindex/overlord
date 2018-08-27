from django import template
import datetime

register = template.Library()

@register.simple_tag
def get_last_year():
	today = datetime.datetime.now()
	return today.year - 1