# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Context
from django.views import generic
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.encoding  import smart_text
from django.core.files import File as DjangoFile
from django.http import Http404

from jfu.http import upload_receive, UploadResponse, JFUResponse
import subprocess, time, sys, os, webodt, io, zipfile

import isasuk.upload.forms as uploadforms
from .forms import *
from .models import File, Proposal
from ..common.helpers import handle_uploaded_file, convert_file, convert_to_pdf, getFilename

templates = {
    'RentContractForm': 'ziadost.odt',
}

def get_context_data(data, form_type):
    if  form_type == 'RentContractForm':
        return {
            'specification': data.get('specification'),
            'identification': data.get('identification'),
            'purpose': data.get('purpose'),
            'price': data.get('price'),
            'period': data.get('period'),
            'reason': data.get('reason'),
            'technical_evaluation': data.get('technical_evaluation'),
       }


def generator_view(request):
    patternform = PatternChoiceForm()
    templateform = None
    link = None
    proposal_id = None
    if 'pattern' in request.POST:
        patternform = PatternChoiceForm(request.POST)
        templateform = getattr(uploadforms, request.POST.get('select_pattern'))()
        proposal_id = request.POST.get('proposal_id')
    elif 'template' in request.POST:
        templateform = getattr(uploadforms, request.POST.get('select_pattern'))(request.POST)
        if templateform.is_valid():
            template = webodt.ODFTemplate(templates.get(request.POST.get('select_pattern')))
            context = get_context_data(request.POST, request.POST.get('select_pattern'))
            document = template.render(Context(context))
            name = convert_to_pdf(document.file.name.split('/')[-1])
            link = getFilename(document.file.name.split('/')[-1]) + '.pdf'
            proposal_id = request.POST.get('proposal_id')
    elif 'save' in request.POST:
        proposal_id = request.POST.get('proposal_id')
        proposal = Proposal.objects.get(id=proposal_id)
        filename = request.POST.get('filename')
        file_instance = File(proposal_id = proposal_id, file_type='proposal', name='Najomna zmluva.pdf')
        file_instance.save()
        file_id = file_instance.id
        if not os.path.isfile(settings.BASE_DIR + '/isasuk/media/' + filename):
          return redirect('/upload/generator/')
        os.makedirs('isasuk/static/storage/docs/'+ str(file_instance.id.hex))
        os.rename(settings.BASE_DIR + '/isasuk/media/' + filename, 'isasuk/static/storage/docs/'+ str(file_instance.id.hex) + '/Najomna zmluva.pdf')
        file = open('isasuk/static/storage/docs/'+ str(file_instance.id.hex) + '/Najomna zmluva.pdf', 'rb')
        d_file = DjangoFile(file)
        file_instance.file = d_file
        file_instance.save()
        file_instance.file.name = 'isasuk/static/storage/docs/'+ str(file_instance.id.hex) + '/Najomna zmluva.pdf'
        file_instance.save()
        convert_file(file_instance)
        proposal.state = 'new'
        proposal.save()
        return render_to_response(
            'upload/success_upload.html',
            context_instance=RequestContext(request)
        )
    else:
        proposal = Proposal(
          name='Najomna zmluva',
          creator=request.user,
          state = 'initial',
        )
        proposal.save()
        proposal_id = proposal.id.hex
    view_data = {
      'patternform': patternform,
      'templateform': templateform,
      'proposal_id': proposal_id,
      'template_type': request.POST.get('select_pattern'),
      'link': link,
    }

    return render_to_response(
      'upload/generator.html',
      view_data,
      context_instance=RequestContext(request)
    )

def upload_view(request):
    uploadform = UploadForm()
    proposal_id = None
    if 'upload_files' in request.POST:
        uploadform = UploadForm(request.POST, request.FILES)
        proposal = Proposal.objects.get(id=request.POST.get('proposal_token'))
        proposal.name = request.POST.get('title')
        proposal.category = request.POST.get('category')
        proposal.state = 'new'
        proposal.save()
        return render_to_response(
            'upload/success_upload.html',
            context_instance=RequestContext(request)
        )
    else:
        proposal = Proposal(
          creator=request.user,
          state = 'initial',
        )
        proposal.save()
        proposal_id = proposal.id.hex

    view_data = {
      'uploadform':uploadform,
      'proposal_id': proposal_id,
    }

    return render_to_response(
      'upload/main.html',
      view_data,
      context_instance=RequestContext(request)
    )


@require_POST
def upload_file( request ):
    file = upload_receive( request )
    instance = File( file = file, proposal_id=request.POST.get('proposal_id'), file_type=request.POST.get('type'), name=file.name.split('/')[-1])
    instance.save()
    convert_file(instance)
    basename = os.path.basename( instance.file.path )

    file_dict = {
        'name' : basename,
        'size' : file.size,
        'deleteUrl': reverse('jfu_delete', kwargs = { 'id': instance.id.hex }),
        'deleteType': 'POST',
    }

    return UploadResponse( request, file_dict )


@require_POST
def delete_file(request, id):
    success = True
    try:
        instance = File.objects.get( id = id )
        os.unlink( instance.file.path )
        instance.delete()
    except UpFile.DoesNotExist:
        success = False

    return JFUResponse( request, success )

def download_file(request, filename):
    path = settings.BASE_DIR + '/isasuk/media/'
    file = open(path + filename, 'rb')
    response = HttpResponse(file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response

def download_original(request, id):
    file_instance = File.objects.get(id=id)
    file = open(file_instance.file.path, 'rb')
    filename = file_instance.file.path.split('/')[-1]
    response = HttpResponse(file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response

def download_pdf(request, id):
    file_instance = File.objects.get(id=id)
    name = getFilename(file_instance.file.path)
    filename = name.split('/')[-1] + '.pdf'
    file = open(name + '.pdf', 'rb')
    response = HttpResponse(file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response

def print_file(request, filename):
    return render_to_response(
      'upload/print.html',
      {'file': filename},
      context_instance=RequestContext(request)
    )

def show_file(request, filename):
    path = settings.BASE_DIR + '/isasuk/media/'
    with open(path + filename, 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response
    pdf.closed

def download_zip(request, proposal_id):
      proposal = Proposal.objects.get(id=proposal_id)
      files = File.objects.filter(proposal_id=proposal_id)
      filenames = []
      for file in files:
        filenames.append(file.file.name)

      zip_subdir = proposal.name
      zip_filename = "%s.zip" % zip_subdir

      s = io.BytesIO()
      zf = zipfile.ZipFile(s, "w")


      zip_subdir = proposal.name
      files = File.objects.filter(proposal_id=proposal_id).exclude(file_type='attachment')
      filenames = []
      for file in files:
        filenames.append(file.file.name)

      for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)

      zip_subdir = proposal.name + '/prílohy'
      files = File.objects.filter(proposal_id=proposal_id, file_type='attachment')
      filenames = []
      for file in files:
        filenames.append(file.file.name)

      for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)

      zf.close()

      resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
      resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

      return resp