from django.utils.translation import ugettext as _
from django import forms

choices = [
  ('','---'),
  ('rent', 'Prenájmy'),
  ('budget', 'Rozpočet'),
  ('agreement', 'Žiadosti o udelenie súhlasu'),
  ('obligation', 'Vecné bremená'),
  ('directive', 'Vnútorná smernica'),
]

patterns = [
  ('','---'),
  ('RentContractForm', 'Nájomná zmluva'),
]

class UploadForm(forms.Form):
    title = forms.CharField(label=_("Názov materiálu"), max_length=80, required=False)
    # main_document = forms.FileField(label=_("Návrh uznesenia"), required=False)
    # own_material = forms.FileField(label=_("Vlastný materiál (vnútorný predpis, koncepcia, správa a pod.)"), required=False)
    # cause = forms.FileField(label=_("Dôvodová správa"), widget=forms.FileInput(), required=False)
    # attachment = forms.FileField(label=_("Sprievodné dokumenty"), required=False)
    category = forms.ChoiceField(label=_("Kategória"), choices=choices, required=False)


class PatternChoiceForm(forms.Form):
    select_pattern = forms.ChoiceField(label=_("Typ zmluvy"), choices=patterns)

class RentContractForm(forms.Form):
    specification = forms.CharField(required=False, widget=forms.Textarea, label=_("Špecifikácia predmetu nájmu"))
    identification = forms.CharField(required=False, widget=forms.Textarea, label=_("Identifikácia nájomcu"))
    purpose = forms.CharField(required=False, widget=forms.Textarea, label=_("Účel nájmu, spôsob a rozsah užívania predmetu nájmu "))
    price = forms.CharField(required=False, widget=forms.Textarea, label=_("Výška nájomného, cena za poskytované služby a dodávku energií "))
    period = forms.CharField(required=False, widget=forms.Textarea, label=_("Doba nájmu"))
    reason = forms.CharField(required=False, widget=forms.Textarea, label=_("Zdôvodnenie výberu nájomcu"))
    technical_evaluation = forms.CharField(required=False, widget=forms.Textarea, label=_("Technické zhodnotenie predmetu nájmu"))




