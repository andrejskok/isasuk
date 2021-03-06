from django.utils.translation import ugettext as _
from django import forms
from isasuk.members.models import Group


def get_all_users():
  users = User.objects.all().order_by('last_name')
  return [(user.id, ' '.join([user.last_name, user.first_name])) for user in users]

def get_user_choices(user):
    groups = Group.objects.filter(member=user, is_chair=True)
    choices = []
    if user.is_superuser:
      return [('ASUK', 'ASUK')]
    for group in groups:
      choices.append((group.group_name, group.group_name))
    return choices

class MeetingForm(forms.Form):
    title =  forms.CharField(label=_("Názov"), max_length=80)
    date = forms.DateTimeField(
      label=_("Dátum"),
      widget=forms.DateTimeInput(
        attrs={'id': 'datetimepicker'},
        format = '%d/%m/%Y %H:%M'),
      input_formats=('%d/%m/%Y %H:%M',))
    choices = forms.ChoiceField()
    invitation = forms.FileField(label=_("Pozvnánka"), required=False, widget=forms.FileInput())


    def __init__(self, *args, **kwargs):
      self.request = kwargs.pop('request', None)
      super(MeetingForm, self).__init__(*args, **kwargs)
      self.fields['choices'] = forms.ChoiceField(label='Typ zasadnutia',choices=get_user_choices(self.request.user))
