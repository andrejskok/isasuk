from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from django import forms
from isasuk.members.models import Group


group_display = {
  'predsednictvo': 'Predsedníctvo AS UK',
  'financna': 'Finančná komisia',
  'pedagogicka': 'Pedagogická komisia',
  'vedecka': 'Vedecká komisia',
  'rozvoj': 'Komisia pre rozvoj',
  'pravna': 'Právna komisia',
  'internaty': 'Komisia pre internáty a ubytovanie',
  'mandatova': 'Mandátová komisia',
  'studentska': 'Študentská časť AS UK',
}

group_names = [
  ('asuk', 'Zasadnutie pléna AS UK'),
  ('predsednictvo', 'Predsedníctvo AS UK'),
  ('financna','Finančná komisia'),
  ('pedagogicka', 'Pedagogická komisia'),
  ('vedecka', 'Vedecká komisia'),
  ('rozvoj', 'Komisia pre rozvoj'),
  ('pravna', 'Právna komisia'),
  ('internaty', 'Komisia pre internáty a ubytovanie'),
  ('mandatova', 'Mandátová komisia'),
  ('studentska', 'Študentská časť AS UK'),
]


def get_all_users():
  users = User.objects.all().order_by('last_name')
  return [(user.id, ' '.join([user.last_name, user.first_name])) for user in users]

def get_user_choices(user):
    groups = Group.objects.filter(member=user, is_chair=True)
    choices = []
    if user.is_superuser:
      return group_names
    for group in groups:
      choices.append((group.group_name, group_display[group.group_name]))
    return choices

class MeetingForm(forms.Form):
    title =  forms.CharField(label=_("Názov"), max_length=256)
    date = forms.DateTimeField(
      label=_("Dátum"),
      widget=forms.DateTimeInput(
        attrs={'id': 'datetimepicker'},
        format = '%d/%m/%Y %H:%M'),
      input_formats=('%d/%m/%Y %H:%M',))
    choices = forms.ChoiceField()
    invited = forms.MultipleChoiceField(label=_("Prizvaní hostia"), widget=forms.CheckboxSelectMultiple, choices=get_all_users())

    def __init__(self, *args, **kwargs):
      self.request = kwargs.pop('request', None)
      super(MeetingForm, self).__init__(*args, **kwargs)
      self.fields['choices'] = forms.ChoiceField(label='Komisia',choices=get_user_choices(self.request.user))
