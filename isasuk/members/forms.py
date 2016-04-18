from django.utils.translation import ugettext as _
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Group

faculties = [('', '-----'),
    ('Pedagogická fakulta', 'Pedagogická fakulta'),
    ('Filozofická fakulta', 'Filozofická fakulta'),
    ('Právnická fakulta', 'Právnická fakulta'),
    ('Prírodovedecká fakulta', 'Prírodovedecká fakulta'),
    ('Fakulta managementu', 'Fakulta managementu'),
    ('Lekárska fakulta', 'Lekárska fakulta'),
    ('Fakulta sociálnych a ekonomických vied', 'Fakulta sociálnych a ekonomických vied'),
    ('Farmaceutická fakulta', 'Farmaceutická fakulta'),
    ('Fakulta telesnej výchovy a športu', 'Fakulta telesnej výchovy a športu'),
    ('Jesseniova lekárska fakulta', 'Jesseniova lekárska fakulta'),
    ('Fakulta matematiky, fyziky a informatiky', 'Fakulta matematiky, fyziky a informatiky'),
    ('Evanjelická bohoslovecká fakulta', 'Evanjelická bohoslovecká fakulta'),
    ('Rímskokatolícka cyrilometodská bohoslovecká fakulta', 'Rímskokatolícka cyrilometodská bohoslovecká fakulta'),
]

titles_before = [('', '-----'),
    ('Bc.', 'Bc.'),
    ('Mgr.', 'Mgr.'),
    ('RNDr.', 'RNDr.'),
    ('doc.', 'doc.'),
    ('prof.', 'prof.'),
]

titles_after = [('', '-----'),
    ('PhD.', 'PhD.'),
    ('CSc.', 'CSc.'),
]


def get_all_users(group_name):
  if not group_name:
    members = []
  else:
    members = Group.objects.all().filter(group_name=group_name).values_list('member__email')
  users = User.objects.filter(details__is_active=True).exclude(email__in=members).order_by('last_name')
  return [('', '----')] + [(user.id, ' '.join([user.first_name, user.last_name])) for user in users]

class AddLeaderForm(forms.Form):
  users = forms.ChoiceField()
  start_leader = forms.DateField(
      label=_("Mandát od"),
      widget=forms.DateInput(format = '%d/%m/%Y', attrs={'placeholder':'dd/mm/RRRR'}),
      input_formats=('%d/%m/%Y', ))
  end_leader = forms.DateField(
      label=_("Mandát do"),
      widget=forms.DateInput(format = '%d/%m/%Y', attrs={'placeholder':'dd/mm/RRRR'}),
      input_formats=('%d/%m/%Y', ))

  def clean_end_leader(self):
    if self.cleaned_data.get('start_leader') and self.cleaned_data.get('end_leader'):
         if self.cleaned_data.get('start_leader') > self.cleaned_data.get('end_leader'):
             raise ValidationError("Koniec musí byť neskôr ako začiatok")
         return self.cleaned_data.get('end_leader')

  def __init__(self, *args, **kwargs):
        group_name = kwargs.pop('group_name')
        super(AddLeaderForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.ChoiceField(label='Používatelia',choices=get_all_users(group_name))

class AddUserForm(forms.Form):
  users = forms.ChoiceField()
  start = forms.DateField(
      label=_("Mandát od"),
      widget=forms.DateInput(format = '%d/%m/%Y', attrs={'placeholder':'dd/mm/RRRR'}),
      input_formats=('%d/%m/%Y', ))
  end = forms.DateField(
      label=_("Mandát do"),
      widget=forms.DateInput(format = '%d/%m/%Y', attrs={'placeholder':'dd/mm/RRRR'}),
      input_formats=('%d/%m/%Y', ))

  def clean_end(self):
          if self.cleaned_data.get('start') and self.cleaned_data.get('end'):
            if self.cleaned_data.get('start') > self.cleaned_data.get('end'):
                raise ValidationError("Koniec musí byť neskôr ako začiatok")
            return self.cleaned_data.get('end')

  def __init__(self, *args, **kwargs):
        group_name = kwargs.pop('group_name')
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.ChoiceField(label='Používatelia',choices=get_all_users(group_name))

class UserForm(forms.Form):
    faculty = forms.ChoiceField(label=_("Fakulta"), choices=faculties, required=False)
    title_before = forms.ChoiceField(label=_("Titul pred menom"), choices=titles_before, required=False)
    title_after = forms.ChoiceField(label=_("Titul za menom"), choices=titles_after, required=False)
    email = forms.EmailField(max_length=40)
    last_name =  forms.CharField(label=_("Priezvisko"), max_length=80)
    first_name = forms.CharField(label=_("Krstné meno"), max_length=80)
    start = forms.DateField(
      label=_("Mandát od"),
      widget=forms.DateInput(format = '%d/%m/%Y', attrs={'placeholder':'dd/mm/RRRR'}),
      input_formats=('%d/%m/%Y', ))
    end = forms.DateField(
      label=_("Mandát do"),
      widget=forms.DateInput(format = '%d/%m/%Y', attrs={'placeholder':'dd/mm/RRRR'}),
      input_formats=('%d/%m/%Y', ))
    is_student = forms.BooleanField(label=_("Študent/Zamestnanec"), initial=False, required=False)
    is_member = forms.BooleanField(label=_("Člen AS"), initial=False, required=False)
    can_submit = forms.BooleanField(label=_("Môže predkladať"), initial=False, required=False)
    is_chair = forms.BooleanField(label=_("Člen Predsedníctva"), initial=False, required=False)

    def clean_end(self):
      if self.cleaned_data.get('start') and self.cleaned_data.get('end'):
            if self.cleaned_data.get('start') > self.cleaned_data.get('end'):
                raise ValidationError("Koniec musí byť neskôr ako začiatok")
            return self.cleaned_data.get('end')

    def clean(self):
        cleaned_data = self.cleaned_data
        unique_email = cleaned_data.get('email')

        if unique_email and len(User.objects.filter(email=unique_email)) > 0:
            raise forms.ValidationError("Not unique email")
        return cleaned_data
