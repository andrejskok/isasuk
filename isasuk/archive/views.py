from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect

from isasuk.upload.models import File, Proposal
from isasuk.negotiation.models import History, Objection

from .forms import SearchForm
import json

def archive_file_view(request, id):
    file_instance = History.objects.get(id=id)
    path = id + "/" + ('.').join(file_instance.name.split('.')[:-1]) + ".html"
    objections = Objection.objects.filter(file_id=id)
    return render_to_response(
        'archive/archive_file.html',
        {
          'path': path,
          'objections': objections,
          'request': request,
          'user': str(request.user.id),
          'file': file_instance,
        },
        context_instance=RequestContext(request)
      )


def archive_view(request):
    searchform = SearchForm()
    results = []
    phrase = ''
    if 'search' in request.POST:
      searchform = SearchForm(request.POST)
      phrase = request.POST.get('name').strip()
      if len(phrase) > 3:
        results = Proposal.objects.filter(state='finished', name__contains=phrase)
      # return HttpResponse()
    return render_to_response(
        'archive/archive.html',
        {
          'phrase': phrase,
          'form': searchform,
          'results': results,
        },
        context_instance=RequestContext(request)
      )

def archive_api(request):
    return HttpResponse()