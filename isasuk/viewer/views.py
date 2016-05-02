from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from ..meeting.models import MeetingsToMaterials, Invited, Meeting
from ..common.helpers import get_proposal_files, getFilename
from isasuk.upload.models import Proposal, File

@login_required
def proposal_view(request, proposal_id, file_id=None):
    proposal = Proposal.objects.get(id=proposal_id)
    if proposal.state == 'finished' and (request.user.is_member or request.user.archive_access):
      print('access_granted')
    elif not request.user.details.is_member and not request.user.details.role == 'admin' and not proposal.creator == request.user:
      meetings_with_material = MeetingsToMaterials.objects.filter(proposal=proposal).values_list('meeting')
      invited = Invited.objects.filter(user=request.user, meeting__in=meetings_with_material)
      if len(invited) == 0:
        return HttpResponse(status=404)
    files = File.objects.filter(proposal_id=proposal_id)
    conclusions = MeetingsToMaterials.objects.filter(proposal=proposal, meeting__closed=True)
    if not file_id:
        files = File.objects.filter(proposal_id=proposal_id)
        if len(files) > 0:
            main_file = files[0]
            file_id = main_file.id.hex
        else:
            raise Http404()
    else:
        main_file = File.objects.get(id=file_id)
    path = file_id + "/" + ('.').join(main_file.name.split('.')[:-1]) + ".html"
    return render_to_response(
        'viewer/main.html',
        {
            'conclusions': conclusions,
            'path': path,
            'proposal': proposal,
            'files': get_proposal_files(proposal_id),
            'file': main_file,
        },
        context_instance=RequestContext(request)
    )

@login_required
def view_document(request, file_id):
    file = File.objects.get(id=file_id)
    if not request.user.details.is_member and not request.user.details.role == 'admin':
      proposal = Proposal.objects.filter(id=file.proposal_id)
      meeting = Meeting.objects.filter(id=file.proposal_id).values_list()
      if len(proposal) > 0:
        if proposal[0].creator != request.user:
          meetings_with_material = MeetingsToMaterials.objects.filter(proposal=proposal[0]).values_list('meeting')
          invited = Invited.objects.filter(user=request.user, meeting__in=meetings_with_material)
          if len(invited) == 0:
            return HttpResponse(status=404)
      elif len(meeting) > 0:
        invited = Invited.objects.filter(user=request.user, meeting__in=[meeting[0]])
        if len(invited) == 0:
          return HttpResponse(status=404)
      else:
        return HttpResponse(status=404)
    path = file_id + "/" + ('.').join(file.name.split('.')[:-1]) + ".html"
    return render_to_response(
        'viewer/viewer.html',
        {
            'path': path,
        },
        context_instance=RequestContext(request)
    )

@login_required
def file_view(request, file_id):
    file = File.objects.get(id=file_id)
    if not request.user.details.is_member and not request.user.details.role == 'admin':
      proposal = Proposal.objects.filter(id=file.proposal_id)
      meeting = Meeting.objects.filter(id=file.proposal_id).values_list()
      if len(proposal) > 0:
        if proposal[0].creator != request.user:
          meetings_with_material = MeetingsToMaterials.objects.filter(proposal=proposal[0]).values_list('meeting')
          invited = Invited.objects.filter(user=request.user, meeting__in=meetings_with_material)
          if len(invited) == 0:
            return HttpResponse(status=404)
      elif len(meeting) > 0:
        invited = Invited.objects.filter(user=request.user, meeting__in=[meeting[0]])
        if len(invited) == 0:
          return HttpResponse(status=404)
      else:
        return HttpResponse(status=404)
    path = file_id + "/" + ('.').join(file.name.split('.')[:-1]) + ".html"
    return render_to_response(
        'viewer/single_file.html',
        {
            'path': path,
            'file': file,
        },
        context_instance=RequestContext(request)
    )

@login_required
def view_senate_docs(request):
    return render_to_response(
        'viewer/senate_docs.html',
        context_instance=RequestContext(request)
    )