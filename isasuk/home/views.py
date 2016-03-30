from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from isasuk.upload.models import File, Proposal
from isasuk.meeting.models import Meeting, MeetingsToMaterials
from isasuk.negotiation.models import Assignement

from ..common.helpers import get_proposal_files
from django.template import Context
import webodt, os
import psutil
from datetime import datetime

def home_view_admin(request, meeting_id):
    return render_to_response('home/main_admin.html')

def home_view_member(request, meeting_id):
    meetings = Meeting.objects.filter(date__gt=datetime.now(), closed=False, state='created').order_by('date')[:5]
    if not meeting_id and len(meetings) > 0:
      url = '/home/' + meetings[0].id.hex
      return redirect(url)

    meeting = Meeting.objects.get(id=meeting_id) if len(meetings) > 0 else []
    my_documents = []
    proposals = Proposal.objects.filter(creator=request.user.id).exclude(state='initial')
    for p in proposals:
      files = File.objects.filter(proposal_id=p.id.hex)
      my_documents.append({
        'proposal': p,
        'files': get_proposal_files(p.id),
      })
    meeting_materials = []
    if meeting:
      assigned_ids = MeetingsToMaterials.objects.filter(meeting=meeting.id.hex).order_by('order')
      for assignement in assigned_ids:
        proposal = Proposal.objects.get(id=assignement.proposal_id)
        meeting_materials.append({
          'proposal': proposal,
          'files': get_proposal_files(proposal.id.hex),
        })
    return render_to_response('home/main.html',
      {
        'documents': my_documents,
        'meeting_materials': meeting_materials,
        'meetings': meetings,
        'id': meeting_id,
        'selected_meeting': meeting,
      },
      context_instance=RequestContext(request),
    )

views_permissions = {
  'home': {
    'admin': home_view_admin,
    'member': home_view_member,
  }
}

def determine_permissions(view, request, meeting_id):
  print(request.user.details.role, meeting_id)
  return views_permissions[view][request.user.details.role](request, meeting_id)


@login_required
def home_view(request, meeting_id=None):
    return determine_permissions('home', request, meeting_id)

