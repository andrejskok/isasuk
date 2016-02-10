from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from isasuk.members.models import Group
from isasuk.upload.models import Proposal, File
from .models import Assignement, Objection, Report, Archive

import os, sys, subprocess, time

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
    proposals = Proposal.objects.filter(state='new')
    files = {}
    for proposal in proposals:
      files[proposal.id] = File.objects.filter(proposal_id=proposal.id)
    return render_to_response(
      'negotiation/negotiation.html',
      {
        'proposals': proposals,
        'files': files,
      },
      context_instance=RequestContext(request)
    )
  elif request.user.details.role == 'member':
    leader = Group.objects.filter(member=request.user, is_chair=True)
    if len(leader) != 0:
      return redirect(reverse('negotiation')+ leader[0].group_name)
    groups = Group.objects.filter(member=request.user, is_chair=False)
    if len(groups) != 0:
      return redirect(reverse('negotiation')+ groups[0].group_name)
    return render_to_response(
      'negotiation/negotiation_member.html',
      {},
      context_instance=RequestContext(request)
    )

def negotiation_group_view(request, group):
  if request.user.details.role == 'member':
    if 'upload' in request.POST:
      proposal_id = request.POST.get('upload')
      assignement = Assignement.objects.get(proposal_id=proposal_id, main_group=group)
      if assignement.group_name != 'predsednictvo':
        print(request.FILES.get('result'), proposal_id)
        file_id= handle_uploaded_file(request, request.FILES.get('result'), proposal_id, 'commission_result')
        print(file_id)
        assignement.group_name = 'predsednictvo'
        assignement.main_group = 'predsednictvo'
        assignement.save()
      else:
        handle_uploaded_file(request, request.FILES.get('files'), proposal_id, 'chair_result')
        assignement.group_name = 'asuk'
        assignement.main_group = 'asuk'
        assignement.save()
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
  if 'assign' in request.POST:
    proposal.state = 'assigned'
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
      'comissions': group_names,
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
    report = Report(reason=reason)
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

def objections_view(request, group, proposal_id, file_id):
    if request.user.details.role == 'member':
      if 'add' in request.POST:
        objection = Objection(
          user_id=request.user,
          file_id=file_id,
          proposal_id=proposal_id,
          original_text=request.POST.get('original_text'),
          objection=request.POST.get('objection'),
          importance=request.POST.get('importance'),
        )
        objection.save()

      if 'upload_revision' in request.POST:
          new_file = request.FILES
          file_type = archive_file(file_id)
          new_file_id = handle_uploaded_file(request, request.FILES.get('revision'), proposal_id, file_type)
          return redirect('/negotiation/'+group+'/'+proposal_id+'/'+new_file_id)
      main_file = File.objects.get(id=file_id)
      leader = Group.objects.filter(member=request.user, is_chair=True)
      groups = Group.objects.filter(member=request.user, is_chair=False)
      proposal = Proposal.objects.get(id=proposal_id)
      archive = Archive.objects.filter(proposal_id=proposal_id, file_type=main_file.file_type).order_by('-timestamp')
      objections = Objection.objects.filter(file_id=file_id).order_by('-importance', '-timestamp')
      files = File.objects.filter(proposal_id=proposal_id)
      files_struct = []
      for f in files:
        obj_count = len(Objection.objects.filter(file_id=f.id))
        files_struct.append({
          'file': f,
          'objections_count': obj_count
          })
      return render_to_response(
        'negotiation/objections.html',
        {
          'path': str(main_file.id) + "/" + ('.').join(main_file.name.split('.')[:-1]) + ".html",
          'archive': archive,
          'request': request,
          'user': str(request.user.id),
          'leader': leader,
          'groups': groups,
          'proposal': proposal,
          'files': files_struct,
          'group_name': group,
          'proposal_id': proposal_id,
          'file_id': file_id,
          'objections': objections,
        },
        context_instance=RequestContext(request)
      )

def objections_redirect_view(request, group, proposal_id):
  main_file = File.objects.filter(proposal_id=proposal_id).get(file_type='proposal')
  return redirect('/negotiation/' + group + '/' + proposal_id + '/' + str(main_file.id))

def archive_file(file_id):
  old_file = File.objects.get(id=file_id)
  file_type = old_file.file_type
  archived_file = Archive(
      id=old_file.id,
      proposal_id=old_file.proposal_id,
      name=old_file.name,
      path='isasuk/static/storage/docs',
      file_type=old_file.file_type,
  )
  old_file.delete()
  archived_file.save()
  return file_type

def handle_uploaded_file(request, f, file_id, file_type):
    if not f:
      return
    file_instance = File(
        proposal_id=file_id,
        name=f.name,
        path='isasuk/static/storage/docs',
        file_type=file_type,
    )
    filename = 'isasuk/static/storage/docs/'+ str(file_instance.id) + '/' + f.name
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    p1 = subprocess.Popen(
        ["powershell.exe",
        "C:\\\"Program Files (x86)\\LibreOffice 4\"\\program\\soffice.exe --headless --convert-to pdf " + "isasuk\\static\\storage\\docs\\" + str(file_instance.id) + "\\" + f.name + " --outdir "  + "isasuk\\static\\storage\\docs\\" + str(file_instance.id)], stdout=sys.stdout)
    p1.wait()
    time.sleep(1)
    p2 = subprocess.Popen(
        ["powershell.exe",
        "D:\\Downloads\\pdf2html\\pdf2htmlEX.exe " + "isasuk\\static\\storage\\docs\\" + str(file_instance.id) + "\\" + ('.').join(f.name.split('.')[:-1]) + ".pdf" + " isasuk\\static\\storage\\docs\\" + str(file_instance.id) + "\\" + ('.').join(f.name.split('.')[:-1]) + ".html"], stdout=sys.stdout)
    p2.wait()
    time.sleep(1)
    file_instance.save()
    return str(file_instance.id)
