from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, Context
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.core.files import File as DjangoFile

from shutil import copyfile
from isasuk.members.models import Group
from .forms import MeetingForm
from .models import Meeting, MeetingsToMaterials
from ..upload.models import Proposal, File
from ..negotiation.models import Assignement
from ..members.models import Group, Attendance
from ..common.helpers import handle_uploaded_file, convert_file, convert_to_pdf, getFilename, get_proposal_files

from jfu.http import upload_receive, UploadResponse, JFUResponse
import datetime, json, os, webodt, time


def meeting_view(request, id):
   meeting = Meeting.objects.get(id=id)
   meeting_materials = []
   assigned_ids = MeetingsToMaterials.objects.filter(meeting=id).order_by('order')
   for assignement in assigned_ids:
     proposal = Proposal.objects.get(id=assignement.proposal_id)
     meeting_materials.append({
       'proposal': proposal,
       'files': get_proposal_files(proposal.id.hex),
     })
   return render_to_response(
     'meeting/meeting.html',
     {
       'meeting': meeting,
       'id': id,
        'meeting_materials': meeting_materials,
     },
     context_instance=RequestContext(request)
     )

def add_meeting_view(request):
  meetingform = MeetingForm(request=request)
  group = Group.objects.filter(member=request.user, is_chair=True)
  if request.user.is_superuser or len(group) > 0:
    successfully_added = False
    if 'add_meeting' in request.POST:
      meetingform = MeetingForm(request.POST, request=request)
      if meetingform.is_valid():
        meeting = add_meeting(request.user.id, request.POST.get('title'), request.POST.get('date'), request.POST.get('choices'))
        proposal_ids = Assignement.objects.filter(group_name=meeting.group)
        ids = [assignement.proposal_id for assignement in proposal_ids]
        proposals = Proposal.objects.filter(id__in = ids)
        return render_to_response(
          'meeting/add_program.html',
          {
              'meeting': meeting,
              'proposals': proposals,
          },
          context_instance=RequestContext(request)
          )
    return render_to_response(
      'meeting/add_meeting.html',
      {
        'form': meetingform,
      },
      context_instance=RequestContext(request)
      )
  else:
    return redirect('/meeting/meetings/')

def my_meetings_view(request):
  success_delete = None
  meetings_leader = []
  meetings_member = []
  is_leader = False
  if "delete" in request.POST:
    id = request.POST.get('id')
    meeting = Meeting.objects.get(id=id)
    meeting.delete()
    success_delete = True
  if request.user.details.role == 'admin':
    meetings_leader = Meeting.objects.filter(closed=False, state='created').order_by('date')
    is_leader = True
  else:
    leader = Group.objects.filter(member=request.user, is_chair=True).values_list('group_name', flat=True)
    groups = Group.objects.filter(member=request.user, is_chair=False).values_list('group_name', flat=True)
    meetings_leader = Meeting.objects.filter(group__in=leader, closed=False, state='created').order_by('date')
    meetings_member = Meeting.objects.filter(group__in=groups, closed=False, state='created').order_by('date')
    is_leader = len(leader) > 0
  #meetings = Meeting.objects.filter(creator=request.user.id, closed=False, state='created').order_by('date')
  return render_to_response(
    'meeting/my_meeting.html',
    {
     'success_delete': success_delete,
     'meetings_leader': meetings_leader,
     'meetings_member': meetings_member,
     'is_leader': is_leader,
    },
    context_instance=RequestContext(request)
  )

def edit_meeting_view(request, id):
  if 'edit' in request.POST:
    return None
  meeting = Meeting.objects.get(id=id)
  proposal_ids = Assignement.objects.filter(group_name=meeting.group)
  assigned_proposal_ids = MeetingsToMaterials.objects.filter(meeting__id=id).order_by('order')
  assigned_ids = [assignement.proposal.id.hex for assignement in assigned_proposal_ids]
  ids = [assignement.proposal_id for assignement in proposal_ids if assignement.proposal_id not in assigned_ids]
  proposals = Proposal.objects.filter(id__in = ids)
  assigned_proposals = []
  for id in assigned_ids:
    assigned_proposals += Proposal.objects.filter(id=id)
  return render_to_response(
    'meeting/edit_meeting.html',
    {
     'meeting': meeting,
     'proposals': proposals,
     'assigned_proposals': assigned_proposals,
    },
    context_instance=RequestContext(request)
  )

def save_meeting_program(request):
  data = request.POST
  ids = json.loads(data.get('ids'))
  meeting_id = request.POST.get('meeting_id')
  MeetingsToMaterials.objects.filter(meeting__id=meeting_id).delete()
  index = 0
  for id in ids:
     meeting_assignement = MeetingsToMaterials(
        meeting=Meeting.objects.get(id=meeting_id),
        proposal=Proposal.objects.get(id=id),
        order=index,
        )
     meeting_assignement.save()
     index += 1
  template = webodt.ODFTemplate('program.odt')
  context = {
    'program': compose_program(meeting_id)
  }
  document = template.render(Context(context))
  file = move_program(document, meeting_id)
  meeting = Meeting.objects.get(id=meeting_id)
  meeting.program = file
  meeting.save()
  return HttpResponse(json.dumps({'success': True}))

def move_program(document, meeting_id):
  tmp = open(document.file.name, 'rb')
  file = DjangoFile(tmp)
  instance = File( file = file, proposal_id=meeting_id, file_type='program', name=file.name.split('\\')[-1])
  instance.save()
  copyfile(file.name, 'isasuk/static/storage/docs/' + instance.id.hex + '/' + file.name.split('\\')[-1])
  instance.file.name = 'isasuk/static/storage/docs/' + instance.id.hex + '/' + file.name.split('\\')[-1]
  instance.save()
  convert_file(instance)
  return instance

def upload_invitation_view(request, id):
  meeting = Meeting.objects.get(id=id)
  invitation = meeting.invitation
  error = False
  if "send" in request.POST:
    if not meeting.invitation:
      error = True
    else:
      meeting.state = 'created'
      meeting.save()
      return redirect(reverse('my_meetings'))
  return render_to_response(
    'meeting/upload_invitation.html',
    { 
      'invitation': meeting.invitation,
      'error': error,
      'meeting_id': id,
    },
    context_instance=RequestContext(request)
  )


def close_meeting_view(request, id):
  meeting = Meeting.objects.get(id=id)
  proposals = MeetingsToMaterials.objects.filter(meeting__id=id)
  attendance = Attendance.objects.filter(meeting__id=id).order_by('user__last_name')
  no_conclusion = False
  saved = False
  if 'close' in request.POST:
    if meeting.conclusion:
      save_attendance(request.POST, id)
      meeting.closed = True
      meeting.save()
      all_materials_assigned = MeetingsToMaterials.objects.filter(meeting=meeting)
      for material in all_materials_assigned:
        if meeting.group == 'asuk':
          material.proposal.state = 'finished'
        else:
          material.proposal.state = 'approved_comission'
        material.proposal.save()
      Assignement.objects.get(proposal_id=material.proposal.id.hex, group_name=meeting.group).delete()
      return redirect(reverse('my_meetings'))
    else:
      no_conclusion = True
  elif 'save' in request.POST:
      save_attendance(request.POST, id)
      saved = True

  return render_to_response(
    'meeting/close_meeting.html',
    { 
      'meeting': meeting,
      'proposals': proposals,
      'attendance': attendance,
      'no_conclusion': no_conclusion,
      'saved': saved,
    },
    context_instance=RequestContext(request)
  )


def save_attendance(data, id):
  attendance = Attendance.objects.filter(meeting__id=id)
  for atendee in attendance:
    if data.get(atendee.id.hex):
      atendee.state = data.get(atendee.id.hex)
    else:
      atendee.state = 'undefined'
    atendee.save()

def add_meeting(creator, title, date, group):
  date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M')
  meeting = Meeting(title=title, date=date, group=group, creator=creator, state='initial')
  meeting.save()
  members = Group.objects.filter(group_name=group)
  for member in members:
    shouldAttend = Attendance(meeting=meeting, user=member.member)
    shouldAttend.save()
  return meeting

@require_POST
def upload_file( request ):
    meeting_id = request.POST.get('proposal_id') # bad naming but it is obvious
    file = upload_receive( request )
    instance = File( file = file, proposal_id=meeting_id, file_type='invitation', name=file.name.split('/')[-1])
    instance.save()
    convert_file(instance)
    basename = os.path.basename( instance.file.path )
    
    meeting = Meeting.objects.get(id=meeting_id) 
    meeting.invitation = instance
    meeting.save()

    file_dict = {
        'name' : basename,
        'size' : file.size,
        'deleteUrl': reverse('invitation_delete', kwargs = { 'id': meeting_id}),
        'deleteType': 'POST',
    }

    return UploadResponse( request, file_dict )

@require_POST
def upload_conclusion_file( request ):
    meeting_id = request.POST.get('proposal_id') # bad naming but it is obvious
    file = upload_receive( request )
    instance = File( file = file, proposal_id=meeting_id, file_type='comission_conclusion', name=file.name.split('/')[-1])
    instance.save()
    convert_file(instance)
    basename = os.path.basename( instance.file.path )
    
    meeting = Meeting.objects.get(id=meeting_id) 
    meeting.conclusion = instance
    meeting.save()

    file_dict = {
        'name' : basename,
        'size' : file.size,
        'deleteUrl': reverse('conclusion_delete', kwargs = { 'id': meeting_id}),
        'deleteType': 'POST',
    }

    return UploadResponse( request, file_dict )

@require_POST
def upload_conclusion_to_material( request ):
    meeting_id = request.POST.get('proposal_id') # bad naming but it is obvious
    file = upload_receive( request )
    instance = File( file = file, proposal_id=meeting_id, file_type='material_conclusion', name=file.name.split('/')[-1])
    instance.save()
    convert_file(instance)
    basename = os.path.basename( instance.file.path )
    meeting = MeetingsToMaterials.objects.get(id=meeting_id) 
    meeting.conclusion = instance
    meeting.save()

    file_dict = {
        'name' : basename,
        'size' : file.size,
        'deleteUrl': reverse('conclusion_material_delete', kwargs = { 'id': meeting_id}),
        'deleteType': 'POST',
    }

    return UploadResponse( request, file_dict )

@require_POST
def delete_file(request, id):
    success = True
    try:
        instance = Meeting.objects.get( id = id )
        instance.invitation.delete()
        instance.save()
    except UpFile.DoesNotExist:
        success = False
    return JFUResponse( request, success )

@require_POST
def delete_conclusion_file(request, id):
    success = True
    try:
        instance = Meeting.objects.get( id = id )
        instance.conclusion.delete()
        instance.save()
    except UpFile.DoesNotExist:
        success = False
    return JFUResponse( request, success )

@require_POST
def delete_conclusion_material(request, id):
    success = True
    try:
        instance = MeetingsToMaterials.objects.get( id = id )
        print(instance)
        print(instance.conclusion)
        instance.conclusion.delete()
        instance.save()
    except UpFile.DoesNotExist:
        success = False
    return JFUResponse( request, success )

def compose_program(meeting_id):
    proposals = MeetingsToMaterials.objects.filter(meeting__id=meeting_id).order_by('order')
    ans = ""
    index = 1
    for proposal in proposals:
      print(proposal.proposal.name)
      ans +=  str(index) + "." + " " + proposal.proposal.name + "\n"
      index += 1
    return ans
