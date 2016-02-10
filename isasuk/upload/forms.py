from django.utils.translation import ugettext as _
from django import forms

choices = [
  ('','---'),
  ('rent', 'Prenájmy'),
  ('budget', 'Rozpočet'),
  ('miscleanous', 'Rôzne'),
]

patterns = [
  ('','---'),
  ('RentContractForm', 'Nájomná zmluva'),
]

class UploadForm(forms.Form):
    title = forms.CharField(label=_("Názov materiálu"), max_length=80)
    main_document = forms.FileField(label=_("Návrh uznesenia"))
    own_material = forms.FileField(label=_("Vlastný materiál (vnútorný predpis, koncepcia, správa a pod.)"))
    cause = forms.FileField(label=_("Dôvodová správa"), required=False, widget=forms.FileInput())
    attachment = forms.FileField(label=_("Sprievodné dokumenty"), required=False)
    organ = forms.FileField(label=_("Vyjadrenie orgánu UK"), required=False)
    category = forms.ChoiceField(label=_("Kategória"), choices=choices, required=False)


class PatternChoiceForm(forms.Form):
    select_pattern = forms.ChoiceField(label=_("Typ šablóny"), choices=patterns)

class RentContractForm(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()




