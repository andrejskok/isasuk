from django import template

register = template.Library()

group_display = {
  'asuk': 'Plénum AS UK',
  'predsednictvo': 'Predsedníctvo AS UK',
  'financna': 'Finančná komisia',
  'pedagogicka': 'Pedagogická komisia',
  'vedecka': 'Vedecká komisia',
  'rozvoj': 'Komisia pre rozvoj',
  'pravna': 'Právna komisia',
  'internaty': 'Komisia pre internáty a ubytovanie',
  'mandatova': 'Mandátová komisia',
}

@register.filter
def getgroupname(key):
  return group_display[key]