from django import template

register = template.Library()

@register.filter
def getextension(filename):
  return filename.split('.')[-1:][0].lower()