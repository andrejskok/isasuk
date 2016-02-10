from django import template

register = template.Library()

filetypes = {
  'commission_result': 'Uznesenie komisie',
  'own_document': 'Vlastný materiál',
  'proposal': 'Návrh',
  'cause': 'Dôvodová žiadosť',
  'organ': 'Vyjadrenie príslušného orgánu',
}

@register.filter
def getfiletype(key):
  return filetypes[key]