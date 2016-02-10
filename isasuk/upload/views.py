from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
import isasuk.upload.forms as uploadforms
from .forms import *
from .models import File, Proposal

import subprocess
import time
import sys
import os

def upload_view(request):
    uploadform = UploadForm()
    patternform = PatternChoiceForm()
    templateform = None

    if 'upload_files' in request.POST:
        uploadform = UploadForm(request.POST, request.FILES)
        if uploadform.is_valid():
            # Create proposal object
            proposal = Proposal(
              creator=request.user,
              state = 'new',
              name = request.POST.get('title'),
            )
            proposal.save()
            # Handle all files from form
            handle_uploaded_file(request, request.FILES['main_document'], proposal.id, 'proposal')
            handle_uploaded_file(request, request.FILES['own_material'], proposal.id, 'own_document')
            handle_uploaded_file(request, request.FILES.get('cause'), proposal.id, 'cause')
            handle_uploaded_file(request, request.FILES.get('organ'), proposal.id, 'organ')
            handle_uploaded_file(request, request.FILES.get('attachment'), proposal.id, 'attachment')

            return render_to_response(
                'upload/success_upload.html',
                context_instance=RequestContext(request)
            ) 

    if 'pattern' in request.POST:
        patternform = PatternChoiceForm(request.POST)
        templateform = getattr(uploadforms, request.POST.get('select_pattern'))()
        '''
        if templateform.is_valid():
            #generate document
            return render_to_response(
                'upload/success_upload.html',
                context_instance=RequestContext(request)
            )
        '''

    view_data = {
    'uploadform':uploadform,
    'patternform': patternform,
    'templateform': templateform,
    }
    print(templateform)

    return render_to_response(
      'upload/main.html',
      view_data,
      context_instance=RequestContext(request)
    )


def handle_uploaded_file(request, f, file_id, file_type):
    if not f:
      return
    file_instance = File(
        proposal_id=file_id,
        name=f.name,
        path='isasuk/static/storage/docs',
        file_type=file_type,
    )
    filename = 'isasuk/static/storage/docs/'+ str(file_instance.id) + '/' + f.name
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # aboslutely temporary
    p1 = subprocess.Popen(
        ["powershell.exe",
        "C:\\\"Program Files (x86)\\LibreOffice 4\"\\program\\soffice.exe --headless --convert-to pdf " + "isasuk\\static\\storage\\docs\\" + str(file_instance.id) + "\\" + f.name + " --outdir "  + "isasuk\\static\\storage\\docs\\" + str(file_instance.id)], stdout=sys.stdout)
    p1.wait()
    time.sleep(1)
    p2 = subprocess.Popen(
        ["powershell.exe",
        "D:\\Downloads\\pdf2html\\pdf2htmlEX.exe " + "isasuk\\static\\storage\\docs\\" + str(file_instance.id) + "\\" + ('.').join(f.name.split('.')[:-1]) + ".pdf" + " isasuk\\static\\storage\\docs\\" + str(file_instance.id) + "\\" + ('.').join(f.name.split('.')[:-1]) + ".html"], stdout=sys.stdout)
    p2.wait()
    time.sleep(1)
    file_instance.save()