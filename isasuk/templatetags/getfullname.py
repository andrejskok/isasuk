from django import template

register = template.Library()

@register.filter
def getfullname(user):
  return ' '.join([user.details.title_before, user.first_name, user.last_name, user.details.title_after]).strip()