from django.shortcuts import render_to_response
from django.template import RequestContext

from isasuk.upload.models import File, Proposal

def objections_view(request):
    files =  None #File.objects.filter(state='new')
    return render_to_response(
        'objections/main.html',
        {
            'files': files,
        },
        context_instance=RequestContext(request)
    )


def document_view(request, id):
    return render_to_response(
        'objections/document_objections.html',
        {
          'id': id,
        },
        context_instance=RequestContext(request)
    )
