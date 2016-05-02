from django.utils.translation import ugettext as _
from django import forms

form_choices = [
  ('rent', 'Žiadosť o udelenie súhlasu s nájmom nehnuteľného majetku'),
  ('prposalRector', 'Návrh rektora na úkony podľa § 41 zákona o VŠ'),
  ('regulationUK', 'Vnútorný predpis UK'),
  ('regulationFaculty', 'Vnútorný predpis fakulty'),
  ('personal', 'Personálny návrh rektora'),
  ('donation', 'Metodika rozpisu dotácií'),
  ('intention', 'Dlhodobý zámer UK'),
  ('report', 'Výročná správa'),
  ('ukscience', 'UK Veda, s.r.o.'),
  ('pricelist', 'Cenník ubytovania'),
  ('other', 'Iné'),
]

choices =   [('','---')] + form_choices

patterns = [
  ('','---'),
  ('RentContractForm', 'Žiadosť o nájom'),
]

class UploadForm(forms.Form):
    title = forms.CharField(label=_("Názov materiálu"), max_length=256, required=False)
    # main_document = forms.FileField(label=_("Návrh uznesenia"), required=False)
    # own_material = forms.FileField(label=_("Vlastný materiál (vnútorný predpis, koncepcia, správa a pod.)"), required=False)
    # cause = forms.FileField(label=_("Dôvodová správa"), widget=forms.FileInput(), required=False)
    # attachment = forms.FileField(label=_("Sprievodné dokumenty"), required=False)
    category = forms.ChoiceField(label=_("Kategória"), choices=choices, required=False)


class PatternChoiceForm(forms.Form):
    select_pattern = forms.ChoiceField(label=_("Typ zmluvy"), choices=patterns)

class RentContractForm(forms.Form):
    specification = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'style': 'resize:vertical'}), label=_("Špecifikácia predmetu nájmu"))
    identification = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'style': 'resize:vertical'}), label=_("Identifikácia nájomcu"))
    purpose = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'style': 'resize:vertical'}), label=_("Účel nájmu, spôsob a rozsah užívania predmetu nájmu "))
    price = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'style': 'resize:vertical'}), label=_("Výška nájomného, cena za poskytované služby a dodávku energií "))
    period = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'style': 'resize:vertical'}), label=_("Doba nájmu"))
    reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'style': 'resize:vertical'}), label=_("Zdôvodnenie výberu nájomcu"))
    technical_evaluation = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'style': 'resize:vertical'}), label=_("Technické zhodnotenie predmetu nájmu"))




