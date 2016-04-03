from django import template

register = template.Library()

@register.filter
def formatresult(name, phrase):
  index = name.lower().index(phrase.lower())
  index2 = index + len(phrase) 
  return name[0:index] + '<strong>' +  name[index:index2] + '</strong>' + name[index2:]