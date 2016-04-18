from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse

from isasuk.members.models import Group
from isasuk.upload.models import Proposal, File
from .models import Assignement, Objection, Report, History
from ..meeting.models import MeetingsToMaterials, Meeting
from jfu.http import upload_receive, UploadResponse, JFUResponse

from ..upload.forms import choices
from ..common.helpers import handle_uploaded_file, convert_file, convert_to_pdf, getFilename, get_proposal_files, rename_and_save
import os, sys, subprocess, time, json

group_names = [
  ('asuk', 'Plénum AS UK'),
  ('predsednictvo', 'Predsedníctvo AS UK'),
  ('financna','Finančná komisia'),
  ('pedagogicka', 'Pedagogická komisia'),
  ('vedecka', 'Vedecká komisia'),
  ('rozvoj', 'Komisia pre rozvoj'),
  ('pravna', 'Právna komisia'),
  ('internaty', 'Komisia pre internáty a ubytovanie'),
  ('mandatova', 'Mandátová komisia'),
  ('studentska', 'Študenstká časť AS UK'),
]

def negotiation_view(request):
  if request.user.details.role == 'admin':
    if 'assign' in request.POST:
      id = request.POST.get('assign')
      url = '/negotiation/assign/' + id
      return redirect(url)
    if 'report' in request.POST:
      id = request.POST.get('report')
      url = '/negotiation/report/' + id
      return redirect(url)
    proposals = Proposal.objects.filter(state__in=['new', 'assigned', 'approved_comission'])
    files = {}
    new = []
    assigned = []
    for proposal in proposals:
      if proposal.state == 'new':
        new.append(proposal)
      else:
        commissions_left = Assignement.objects.filter(proposal_id=proposal.id.hex).values_list('group_name', flat=True)
        commissions_done = MeetingsToMaterials.objects.filter(proposal=proposal, meeting__closed=True).values_list('meeting__group', flat=True)
        assigned.append({
          'proposal': proposal,
          'left': commissions_left,
          'done': commissions_done,
          'done_all': len(commissions_left) == 0,
        })
    return render_to_response(
      'negotiation/negotiation.html',
      {
        'proposals': proposals,
        'new': new,
        'assigned': assigned,
        'files': files,
      },
      context_instance=RequestContext(request)
    )
  elif request.user.details.role == 'member':
    groups = Group.objects.filter(member=request.user).values_list('group_name', flat=True)
    meetings = Meeting.objects.filter(group__in=groups, closed=True)
    return render_to_response(
      'negotiation/negotiation_member.html',
      {
        'meetings': meetings,
      },
      context_instance=RequestContext(request)
    )

def negotiation_group_view(request, group):
  if request.user.details.role == 'member':
    leader = Group.objects.filter(member=request.user, is_chair=True)
    groups = Group.objects.filter(member=request.user, is_chair=False)
    is_leader = len(Group.objects.filter(member=request.user, group_name=group, is_chair=True)) > 0
    assigned = Assignement.objects.filter(group_name=group)
    proposals = []
    for a in assigned:
      proposal = Proposal.objects.get(id=a.proposal_id)
      proposals.append((proposal.id, proposal))
    return render_to_response(
      'negotiation/negotiation_member.html',
      {
      'is_leader': is_leader,
      'leader': leader,
      'groups': groups,
      'proposals': proposals,
      'name': group,
      },
      context_instance=RequestContext(request)
    )


def assign_view(request, id):
  if request.user.details.role != 'admin':
    return None
  proposal = Proposal.objects.get(id=id)
  files = get_proposal_files(id)
  if 'assign' in request.POST:
    proposal.state = 'assigned'
    proposal.save()
    if files['proposal']:
        name = request.POST.get(files['proposal'].id.hex)
        rename_and_save(files['proposal'], name)
    if files['own_material']:
        name = request.POST.get(files['own_material'].id.hex)
        rename_and_save(files['own_material'], name)
    for file in files['attachment']:
        name = request.POST.get(file.id.hex)
        rename_and_save(file, name)
    category = request.POST.getlist('category')
    proposal.category = category
    proposal.save()
    groups = request.POST.getlist('comission')
    main_group = request.POST.get('gestor')
    for group in groups:
      if group != main_group:
        assignement = Assignement(proposal_id=id, group_name=group, main_group=False)
        assignement.save()
    assignement = Assignement(proposal_id=id, group_name=main_group, main_group=True)
    assignement.save()
    return render_to_response(
      'negotiation/negotiation_assign_success.html',
      {},
      context_instance=RequestContext(request)
    )
  return render_to_response(
      'negotiation/negotiation_assign.html',
      {
      'proposal': proposal,
      'files': files,
      'comissions': group_names,
      'choices': choices,
      },
      context_instance=RequestContext(request)
    )

def report_view(request, id):
  if request.user.details.role != 'admin':
    return None
  proposal = Proposal.objects.get(id=id)
  if 'report' in request.POST:
    proposal.state = 'reported'
    proposal.save()
    reason = request.POST.get('reason')
    report = Report(reason=reason, proposal_id=id)
    report.save()
    return render_to_response(
      'negotiation/negotiation_assign_success.html',
      {},
      context_instance=RequestContext(request)
    )
  return render_to_response(
      'negotiation/negotiation_report.html',
      {
      'proposal': proposal,
      },
      context_instance=RequestContext(request)
    )

def objections_view(request, meeting_id, file_id):
    if request.user.details.role == 'member':
      if 'add' in request.POST:
        objection = Objection(
          user_id=request.user,
          file_id=file_id,
          original_text=request.POST.get('original_text'),
          objection=request.POST.get('objection'),
          importance=request.POST.get('importance'),
        )
        objection.save()
      if 'save_revision' in request.POST:
          new_file = File.objects.get(id=request.POST.get('id'))
          meeting = Meeting.objects.get(id=meeting_id)
          file_type = archive_file(meeting.conclusion.id.hex, meeting_id)
          meeting.conclusion = new_file
          meeting.save()
          return HttpResponse(json.dumps({'success': True, 'url': 'negotiation/' + meeting_id + '/' + new_file.id.hex}))
      meeting = Meeting.objects.get(id=meeting_id)
      main_file = File.objects.get(id=file_id)
      history = History.objects.filter(meeting_id=meeting_id).order_by('-timestamp')
      objections = Objection.objects.filter(file_id=file_id).order_by('-importance', '-timestamp')
      d = {
          'path': main_file.id.hex + "/" + ('.').join(main_file.name.split('.')[:-1]) + ".html",
          'history': history,
          'request': request,
          'user': str(request.user.id),
          'meeting': meeting,
          'file_id': file_id,
          'objections': objections,
        }
      print(d)
      return render_to_response(
        'negotiation/objections.html',
        d,
        context_instance=RequestContext(request)
      )

def objections_redirect_view(request, group, proposal_id):
  main_file = File.objects.filter(proposal_id=proposal_id).get(file_type='proposal')
  return redirect('/negotiation/' + group + '/' + proposal_id + '/' + str(main_file.id))

def archive_file(file_id, meeting_id):
  old_file = File.objects.get(id=file_id)
  file_type = old_file.file_type
  archived_file = History(
      id=old_file.id,
      meeting_id=meeting_id,
      name=old_file.name,
      path='isasuk/static/storage/docs',
      file_type=old_file.file_type,
  )
  old_file.delete()
  archived_file.save()
  return file_type

@require_POST
def upload_file( request ):
    file = upload_receive( request )
    instance = File( file = file, proposal_id=request.POST.get('proposal_id'), file_type=request.POST.get('type'), name=file.name.split('/')[-1])
    instance.save()
    convert_file(instance)
    basename = os.path.basename( instance.file.path )

    file_dict = {
        'name' : basename,
        'size' : file.size,
        'deleteUrl': reverse('negotiation_delete', kwargs = { 'id': instance.id.hex }),
        'deleteType': 'POST',
    }

    return UploadResponse( request, file_dict )

@require_POST
def delete_file(request, id):
    success = True
    try:
        instance = File.objects.get( id = id )
        os.unlink( instance.file.path )
        instance.delete()
    except UpFile.DoesNotExist:
        success = False

    return JFUResponse( request, success )
