from django import template

register = template.Library()

@register.filter
def formattext(text, phrase):
  index = text.lower().index(phrase.lower())
  index2 = index + len(phrase)
  return '...' + text[max(index-15, 0):index] + '<strong>' +  text[index:index2] + '</strong>' + text[index2:min(index2+15, len(text))] + '...'