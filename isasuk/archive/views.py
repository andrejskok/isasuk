from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect

from isasuk.upload.models import File
from isasuk.negotiation.models import Archive, Objection

def archive_view(request, id):
    file_instance = Archive.objects.get(id=id)
    path = id + "/" + ('.').join(file_instance.name.split('.')[:-1]) + ".html"
    objections = Objection.objects.filter(file_id=id)
    return render_to_response(
        'archive/archive.html',
        {
          'path': path,
          'objections': objections,
          'request': request,
          'user': str(request.user.id),
          'file': file_instance,
        },
        context_instance=RequestContext(request)
      )
