from django import template

register = template.Library()

statetypes = {
  'new': 'Nový',
  'reported': 'Nahlásený',
  'assigned': 'Priradený komisií',
  'meeting': 'Na prerokovanie v AS UK',
  'approved': 'Schválený',
}

@register.filter
def getstate(key):
  return statetypes[key]