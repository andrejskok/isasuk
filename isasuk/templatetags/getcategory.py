from django import template

register = template.Library()

categories = {
  'rent': 'Žiadosť o udelenie súhlasu s nájmom nehnuteľného majetku',
  'prposalRector': 'Návrh rektora na úkony podľa § 41 zákona o VŠ',
  'regulationUK': 'Vnútorný predpis UK',
  'regulationFaculty': 'Vnútorný predpis fakulty',
  'personal': 'Personálny návrh rektora',
  'donation': 'Metodika rozpisu dotácií',
  'intention': 'Dlhodobý zámer UK',
  'report': 'Výročná správa',
  'ukscience': 'UK Veda: s.r.o.',
  'pricelist': 'Cenník ubytovania',
  'other': 'Iné',
}

@register.filter
def getcategory(category):
  ans = categories.get(category)
  return ans if ans else ''