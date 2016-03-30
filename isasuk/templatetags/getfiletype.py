from django import template

register = template.Library()

filetypes = {
  'commission_result': 'Uznesenie komisie',
  'own_material': 'Vlastný materiál',
  'proposal': 'Návrh',
  'cause': 'Dôvodová žiadosť',
  'organ': 'Vyjadrenie príslušného orgánu',
  'attachment': 'Prílohy',
  'docs': 'Sprievodné dokumenty',
}

@register.filter
def getfiletype(key):
  return filetypes[key]