from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.models import Count
from isasuk.accounts.models import Details
from isasuk.upload.models import File, Proposal
from isasuk.members.models import Group, AdhocGroup
from .forms import UserForm, AddUserForm
import pprint
import mandrill
mandrill_client = mandrill.Mandrill('vWEYy5TI1BFYISDBXOIJyA')

group_names = [
  ('predsednictvo', 'Predsedníctvo AS UK'),
  ('financna','Finančná komisia'),
  ('pedagogicka', 'Pedagogická komisia'),
  ('vedecka', 'Vedecká komisia'),
  ('rozvoj', 'Komisia pre rozvoj'),
  ('pravna', 'Právna komisia'),
  ('internaty', 'Komisia pre internáty a ubytovanie'),
  ('mandatova', 'Mandátová komisia'),
]

group_display = {
  'predsednictvo': 'Predsedníctvo AS UK',
  'financna': 'Finančná komisia',
  'pedagogicka': 'Pedagogická komisia',
  'vedecka': 'Vedecká komisia',
  'rozvoj': 'Komisia pre rozvoj',
  'pravna': 'Právna komisia',
  'internaty': 'Komisia pre internáty a ubytovanie',
  'mandatova': 'Mandátová komisia',
}

def send_verification_email(id, email):
    url = 'localhost:8000/members/verify/' + str(id)
    message = {
          'from_email': 'registracia@sportrank.sk',
          'from_name': 'IS AS UK',
          'to': [{'email': email}],
          'html': 'Vitajte v systeme<a>' + url + '</a>',
      }
    mandrill_client.messages.send(message=message)

def members_view(request):
    members = User.objects.all()
    if request.user.details.role == 'member':
        return render_to_response(
        'members/members.html',
        {
          'members_active': 'active',
          'data': members,
        },
        context_instance=RequestContext(request)
    )
    elif request.user.details.role == 'admin':
        successfull_user_addition = False
        successfull_user_removal = False
        successfull_user_edit = False
        userform = UserForm()
        if 'add_user' in request.POST:
            userform = UserForm(request.POST)
            if userform.is_valid():
                id = add_user(request.POST)
                send_verification_email(id, request.POST.get('email'))
                successfull_user_addition = True
                userform = UserForm()
        print(request.POST)
        if 'remove' in request.POST:
              remove_user(request.POST.get('id'))
              successfull_user_removal = True
        if 'save_edit' in request.POST:
              edit_user(request)
              successfull_user_edit = True
        return render_to_response(
        'members/admin_members.html',
        {
          'members_active': 'active',
          'data': members,
          'userform': userform,
          'user': request.user,
          'successfull_user_edit': successfull_user_edit,
          'successfull_user_removal': successfull_user_removal,
          'successfull_user_addition': successfull_user_addition,
        },
        context_instance=RequestContext(request)
    )


def groups_view(request, group_name=None):
    names = [i[0] for i in group_names]
    if group_name not in names:
      return redirect('/members/groups/financna/')
    if request.user.details.role == 'member':
        group_members =  Group.objects.filter(group_name=group_name).exclude(is_chair=True)
        group_leader =  Group.objects.filter(group_name=group_name).filter(is_chair=True)

        if len(group_leader) == 0:
          group_leader = None
        else:
          group_leader = group_leader[0]
        return render_to_response(
        'members/member_groups.html',
        {
          'groups_active': 'active',
          'group_members': group_members,
          'group_leader': group_leader,
          'group_name': group_name,
          'group_names': group_names,
          'display_name': group_display[group_name],
        },
        context_instance=RequestContext(request)
    )
    elif request.user.details.role == 'admin':
        if 'add_user' in request.POST:
          add_user_to_group(request.POST.get('users'), group_name)
        if 'add_leader' in request.POST:
          add_leader_to_group(request.POST.get('users'), group_name)
        if 'remove' in request.POST:
          remove_user_from_group(request.POST.get('id'), group_name)
        if 'remove_leader' in request.POST:
          remove_leader_from_group(request.POST.get('id'), group_name)

        group_members =  Group.objects.filter(group_name=group_name).exclude(is_chair=True)
        group_leader =  Group.objects.filter(group_name=group_name).filter(is_chair=True)

        if len(group_leader) == 0:
          group_leader = None
        else:
          group_leader = group_leader[0]
        return render_to_response(
        'members/groups.html',
        {
          'groups_active': 'active',
          'group_members': group_members,
          'group_leader': group_leader,
          'group_name': group_name,
          'group_names': group_names,
          'display_name': group_display[group_name],
          'form': AddUserForm(),
        },
        context_instance=RequestContext(request)
    )

def password_view(request, id):
    success = False
    if 'submit' in request.POST:
      password = request.POST.get('password')
      re_password = request.POST.get('re_password')
      if password and password == re_password:
        user = User.objects.get(id=id)
        print(user)
        user.set_password(password)
        print(user.password)
        user.save()
        return redirect(reverse('login'))
    return render_to_response(
        'members/password_set.html',
        {},
        context_instance=RequestContext(request))

def adhoc_view(request):
    if request.user.details.role == 'member':
        members = User.objects.all()
        return render_to_response(
        'members/main.html',
        {
          'adhoc_active': 'active',
          'members': members,
        },
        context_instance=RequestContext(request)
    )

def add_user(data):
    user = User(
       email = data['email'],
       username= data['email'],
       first_name = data['first_name'],
       last_name = data['last_name'],
    )
    user.save()
    member = Details(
        user=user,
        role = 'member',
        start = data['start'],
        end = data['end'],
        is_student = check_boolean_field(data, 'is_student'),
        is_member = check_boolean_field(data, 'is_member'),
        can_submit = check_boolean_field(data, 'can_submit'),
        is_chair = check_boolean_field(data, 'is_chair'), 
    )
    member.save()
    return user.id

def edit_user(request):
  data = request.POST
  user = User.objects.get(id=data['id'])
  details = user.details
  details.is_student = check_boolean_field(data, 'is_student')
  details.is_member = check_boolean_field(data, 'is_member')
  details.can_submit = check_boolean_field(data, 'can_submit')
  details.is_chair = check_boolean_field(data, 'is_chair')
  details.save()

def check_boolean_field(data, field):
    if data.get(field) is None:
      return False
    return True

def remove_user(id):
    User.objects.get(id=id).delete()

def add_user_to_group(id, group):
    present = Group.objects.filter(group_name=group).filter(member=id)
    if len(present) > 0:
      return 
    group = Group(
      member=User.objects.get(id=id),
      group_name=group,
      is_chair=False,
    )
    group.save()

def remove_user_from_group(id, group):
    Group.objects.filter(group_name=group).filter(member=id).delete()


def add_leader_to_group(id, group):
    leader = Group.objects.filter(group_name=group).filter(member=id)
    if len(leader) == 0:
      add_user_to_group(id, group)
    leader = Group.objects.filter(group_name=group).get(member=id)
    leader.is_chair = True
    leader.save()

def remove_leader_from_group(id, group):
    Group.objects.filter(group_name=group).get(member=id).delete()