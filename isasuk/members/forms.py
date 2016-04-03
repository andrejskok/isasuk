from django.utils.translation import ugettext as _
from django import forms
from django.contrib.auth.models import User

def get_all_users():
  users = User.objects.filter(details__is_active=True).order_by('last_name')
  return [(user.id, ' '.join([user.first_name, user.last_name])) for user in users]

class AddUserForm(forms.Form):
  users = forms.ChoiceField()

  def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.ChoiceField(label='Používatelia',choices=get_all_users())

class UserForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=40)
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
    is_student = forms.BooleanField(label=_("Študent"), initial=False, required=False)
    is_member = forms.BooleanField(label=_("Člen AS"), initial=False, required=False)
    can_submit = forms.BooleanField(label=_("Môže predkladať"), initial=False, required=False)
    is_chair = forms.BooleanField(label=_("Člen Predsedníctva"), initial=False, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        unique_email = cleaned_data.get('email')

        if unique_email and len(User.objects.filter(email=unique_email)) > 0:
            raise forms.ValidationError("Not unique email")
        return cleaned_data
