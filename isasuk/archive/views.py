from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from isasuk.upload.models import File, Proposal
from isasuk.negotiation.models import History, Objection
from .models import ArchiveDocs

from ..meeting.models import Meeting
from .forms import SearchDocumentForm, SearchMeetingsForm
import json
from datetime import datetime

@login_required
def archive_file_view(request, id):
    if request.user.details.is_member or request.user.details.archive_access:
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
    else:
      return HttpResponse(status=404)

@login_required
def archive_view(request):
    if request.user.details.is_member or request.user.details.archive_access:
      searchform = SearchDocumentForm()
      documents_available = []
      docs = False
      search = False
      results = []
      phrase = ''
      if 'search' in request.POST:
        searchform = SearchDocumentForm(request.POST)
        if searchform.is_valid():
          selected = searchform.cleaned_data['doc_type']
          phrase = searchform.cleaned_data['name'].strip()
          if phrase and len(phrase) > 3:
            results = Proposal.objects.filter(name__contains=phrase)
            search = True
          else:
            results = Proposal.objects.all()
          if request.POST.get('docs'):
             docs = True
          if request.POST.get('docs') and len(phrase) > 3:
            archived = ArchiveDocs.objects.all()
            filtered_files = []
            for archive in archived:
              proposal = Proposal.objects.filter(id=archive.file.proposal_id)  # better is get, legacy code
              if len(proposal) > 0 and proposal[0].state == 'finished':
                filtered_files.append(archive.file)
            documents_available = ArchiveDocs.objects.filter(text__contains=phrase)
          if selected:
            results = results.filter(category__in=selected)
      return render_to_response(
          'archive/archive.html',
          {
            'search': search,
            'phrase': phrase,
            'form': searchform,
            'results': results,
            'docs': docs,
            'documents': documents_available,
          },
          context_instance=RequestContext(request)
        )
    return HttpResponse(status=404)

@login_required
def meetings_view(request):
    if request.user.details.is_member or request.user.details.archive_access:
      form = SearchMeetingsForm()
      results = Meeting.objects.all().filter(date__lt=datetime.now()).order_by('-date')[0:10]
      length = len(Meeting.objects.all()) - 10
      if 'all' in request.POST:
        results = Meeting.objects.all().filter(date__lt=datetime.now()).order_by('-date')
        length = 0
      if 'filter' in request.POST:
        results = Meeting.objects.all().filter(date__lt=datetime.now()).order_by('-date')
        form = SearchMeetingsForm(request.POST)
        if form.is_valid():
          if form.cleaned_data['commission']:
            results = results.filter(group__in=form.cleaned_data['commission'])
          #commissions = form.cleaned_data['commission']
          #for commission in commissions:
          #  results[commission] = Meeting.objects.filter(group=commission).order_by('-date') # filter closed
          if form.cleaned_data['start']:
            results = results.filter(date__gt=form.cleaned_data['start'])
          if form.cleaned_data['end']:
            results = results.filter(date__lt=form.cleaned_data['end'])
      return render_to_response(
          'archive/meeting_archive.html',
          {
            'length': length,
            'form': form,
            'results': results,
          },
          context_instance=RequestContext(request)
        )
    else:
      return HttpResponse(status=404)
