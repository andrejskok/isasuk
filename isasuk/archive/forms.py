from django.utils.translation import ugettext as _
from django import forms

from ..upload.forms import form_choices as choices
from ..meeting.forms import group_names


class SearchDocumentForm(forms.Form):
    name = forms.CharField(label=_("Názov"), max_length=256, required=False)
    doc_type = forms.MultipleChoiceField(label=_("Typ materiálu"), choices = choices, widget = forms.CheckboxSelectMultiple, required=False)


class SearchMeetingsForm(forms.Form):
    commission = forms.MultipleChoiceField(label=_("Komisia"), choices = group_names, widget = forms.CheckboxSelectMultiple, required=False)
    start = forms.DateField(
        label=_("Od"),
        widget=forms.DateInput(format = '%d/%m/%Y', attrs={'placeholder':'dd/mm/RRRR'}),
        input_formats=('%d/%m/%Y', ), required = False)
    end = forms.DateField(
        label=_("Do"),
        widget=forms.DateInput(format = '%d/%m/%Y', attrs={'placeholder':'dd/mm/RRRR'}),
        input_formats=('%d/%m/%Y', ), required = False)
