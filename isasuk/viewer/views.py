from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse

from ..meeting.models import MeetingsToMaterials
from ..common.helpers import get_proposal_files, getFilename
from isasuk.upload.models import Proposal, File

def proposal_view(request, proposal_id, file_id=None):
    proposal = Proposal.objects.get(id=proposal_id)
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

def view_document(request, file_id):
    file = File.objects.get(id=file_id)
    path = file_id + "/" + ('.').join(file.name.split('.')[:-1]) + ".html"
    return render_to_response(
        'viewer/viewer.html',
        {
            'path': path,
        },
        context_instance=RequestContext(request)
    )

def file_view(request, file_id):
    file = File.objects.get(id=file_id)
    path = file_id + "/" + ('.').join(file.name.split('.')[:-1]) + ".html"
    return render_to_response(
        'viewer/single_file.html',
        {
            'path': path,
            'file': file,
        },
        context_instance=RequestContext(request)
    )