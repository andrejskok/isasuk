from django.shortcuts import render_to_response
from django.template import RequestContext

from isasuk.upload.models import Proposal, File

def proposal_view(request, proposal_id, file_id):
    proposal = Proposal.objects.get(id=proposal_id)
    files = File.objects.filter(proposal_id=proposal_id)
    main_file = File.objects.get(id=file_id)
    path = file_id + "/" + ('.').join(main_file.name.split('.')[:-1]) + ".html"
    return render_to_response(
        'viewer/main.html',
        {
            'path': path,
            'proposal': proposal,
            'files': files,
            'file': main_file,
        },
        context_instance=RequestContext(request)
    )

def document_view(request, id):
    file_instance = File.objects.get(id=id)
    print(file_instance.path + '/' + id + '/' + file_instance.name, file=sys.stderr) 
    return render_to_response(
        'viewer/dohoda123.html',
        context_instance=RequestContext(request)
    )


def path_view(request, path):
    return render_to_response(
        path,
        {'path': path},
        context_instance=RequestContext(request)
    )