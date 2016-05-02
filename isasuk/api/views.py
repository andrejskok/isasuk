from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from ..upload.models import File, Proposal
from ..archive.models import ArchiveDocs
from ..meeting.models import Meeting, MeetingsToMaterials
from ..common.helpers import getFilename
import json
from datetime import datetime

def login_user(request):
    if 'submit' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user and user.details.is_active is False:
            return None
        return user
    return None

def login(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({'success': False}))
    else:
        t = login_user(request)
        if t is not None:
            login(request, t)
            return HttpResponse(json.dumps({'success': True}))
    return HttpResponse(json.dumps({'success': False}))

def logout(request):
    logout(request)
    return HttpResponse(json.dumps({'success': True}))

@login_required
def users(request):
    if request.user.is_authenticated():
      return HttpResponse(json.dumps({'error': 'not authenticated'}))
    result = User.objects.all()
    users = []
    for user in result:
      users.append({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.username,
        'id': user.id,
        })
    return HttpResponse(json.dumps(users))

@login_required
def meetings(request):
    if request.user.is_authenticated():
      return HttpResponse(json.dumps({'error': 'not authenticated'}))
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    commissions = json.loads(request.POST.get('commissions'))
    result = Meeting.objects.filter(closed=True)
    ans = []
    if date_from:
      result = result.filter(date__gt=date_from)
    if date_to:
      result = result.filter(date__lt=date_to)
    if len(commissions) > 0:
      result = result.filter(group__in=commissions)
    for meeting in results:
      ans.append({
        'id': meeting.id.hex,
        'date': meeting.date,
        'group': meeting.group,
        'invitation': meeting.invitation.id.hex,
        'program': meeting.program.id.hex,
      })
    return HttpResponse(json.dumps(result))

@login_required
def materials(request):
    if request.user.is_authenticated():
      return HttpResponse(json.dumps({'error': 'not authenticated'}))
    search = request.POST.get('search')
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    categories = json.loads(request.POST.get('categories'))
    proposed_by = request.POST.get('proposed_by')
    result = Materials.objects.filter(state='finished')
    ans = []
    if proposed_by:
      result = result.filter(creator__id=proposed_by)
    if len(categories) > 0:
      result = result.filter(category__in=categories)
    if date_from:
      result = result.filter(date__gt=date_from)
    if date_to:
      result = result.filter(date__lt=date_to)
    if len(search) > 3:
      result = result.filter(name__contains=search)
    for material in result:
      ans.append({
        'id': material.id.hex,
        'name': material.name,
        'proposed_by': material.creator.id,
        'timestamp': material.timestamp,
      })
    return HttpResponse(json.dumps(ans))

@login_required
def material(request, id):
    if request.user.is_authenticated():
      return HttpResponse(json.dumps({'error': 'not authenticated'}))
    material = Proposal.objects.filter(id = id)
    if len(material) != 1:
      return HttpResponse(json.dumps({'error': 'nonexisting id'}))
    files = File.object.filter(proposal_id = id)
    additional = MeetingsToMaterials.objects.filter(proposal__id = id, meeting__closed = True)
    materials = []
    additional_documents = []
    for file in files:
      if file.file_type in []:
        materials.append({
          'id': file.id.hex,
          'file_type': file.file_type,
          'proposed_by': material.creator.id,
          'timestamp': file.timestamp,
        })
      else:
        additional_documents.append({
          'id': file.id.hex,
          'file_type': file.file_type,
          'timestamp': file.timestamp,
        })
    for file in additional:
      conclusion = file.conclusion if file.conclusion else file.meeting.conclusion
      additional_documents.append({
        'id': conclusion.id.hex,
        'file_type': conclusion.file_type,
        'commissions': file.meeting.group,
        'timestamp': conclusion.timestamp,
      })

    return HttpResponse(json.dumps({
      'name': material.name,
      'proposed_by': material.creator.id,
      'timestamp': material.timestamp,
      'material': materials,
      'additional_documents': additional_documents,
    }))

@login_required
def file(request, id):
    if request.user.is_authenticated():
      return HttpResponse(json.dumps({'error': 'not authenticated'}))
    file_instance = File.objects.get(id=id)
    name = getFilename(file_instance.file.path)
    filename = name.split('/')[-1] + '.pdf'
    file = open(name + '.pdf', 'rb')
    response = HttpResponse(file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response
