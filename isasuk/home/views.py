from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from isasuk.upload.models import File, Proposal
from isasuk.meeting.models import Meeting
from isasuk.negotiation.models import Assignement

def home_view_admin(request, meeting_id):
    return render_to_response('home/main_admin.html')

def home_view_member(request, meeting_id):
    meetings = Meeting.objects.all().order_by('date')
    if not meeting_id and len(meetings) > 0:
      url = '/home/' + meetings[0].id.hex
      return redirect(url)
    meeting = Meeting.objects.filter(id=meeting_id)
    documents = []
    proposals = Proposal.objects.filter(creator=request.user.id)
    for p in proposals:
      files = File.objects.filter(proposal_id=p.id)
      documents.append({
        'proposal': p,
        'files': files,
      })

    actual = []
    if meeting:
      meeting = meeting[0]
      assigned = Assignement.objects.filter(group_name=meeting.group)
      for a in assigned:
        proposal = Proposal.objects.get(id=a.proposal_id)
        files = File.objects.filter(proposal_id=proposal.id)
        actual.append({
          'proposal': proposal,
          'files': files,
        })
    return render_to_response('home/main.html',
      {'documents': documents, 'actual': actual, 'meetings': meetings, 'id': meeting_id},
      context_instance=RequestContext(request),
    )

views_permissions = {
  'home': {
    'admin': home_view_admin,
    'member': home_view_member,
  }
}

def determine_permissions(view, request, meeting_id):
  return views_permissions[view][request.user.details.role](request, meeting_id)


@login_required
def home_view(request, meeting_id=None):
    return determine_permissions('home', request, meeting_id)

