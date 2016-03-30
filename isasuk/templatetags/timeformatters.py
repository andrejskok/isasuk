from django import template

register = template.Library()

@register.filter
def gettime(date):
  return date

@register.filter
def getdate(date):
  return date