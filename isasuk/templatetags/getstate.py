from django import template

register = template.Library()

statetypes = {
  'new': 'Nový',
  'reported': 'Nahlásený',
  'assigned': 'Priradený komisií',
  'assigned_asuk': 'Priradený plénu AS UK',
  'approved_comission': 'Prerokovaný v komisií',
  'finished': 'Prerokovanie v pléne UK ukončené',
}

@register.filter
def getstate(key):
  return statetypes[key]