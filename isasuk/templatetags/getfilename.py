from django import template

register = template.Library()

@register.filter
def getfilename(filename):
  return ('.').join(filename.split('.')[:-1])