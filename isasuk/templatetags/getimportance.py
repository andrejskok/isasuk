from django import template

register = template.Library()

importrance = {
  '1': 'Nízka',
  '2': 'Stredná',
  '3': 'Vysoká',
}

@register.filter
def getimportance(key):
  return importrance[key]