from django import template

register = template.Library()

@register.filter
def keyvalue(dict, key):
  return dict[key]

@register.filter
def lookup(d, key):
    print(d, key)
    return d[key-1]