rom ..upload.models import File
from django.core.files import File as DjangoFile
from django.conf import settings

import subprocess
import sys
import os

def getFilename(filename):
  return ('.').join(filename.split('.')[:-1])

def getExtension(filename):
  return filename.split('.')[-1:][0].lower()

def get_proposal_files(id):
   files = File.objects.filter(proposal_id=id)
   proposal = files.filter(file_type='proposal')
   own_material = files.filter(file_type='own_material')
   docs = files.filter(file_type='docs')
   attachment = files.filter(file_type='attachment')
   return {
        'proposal': proposal[0] if proposal else proposal,
        'own_material': own_material[0] if own_material else own_material,
        'attachment': attachment,
        'docs': docs,
   }

def rename_and_save(file, name):
  extension = getExtension(file.file.path)
  path = '/'.join(file.file.path.split('/')[0:-1])
  new_path =  os.path.join(path, name) + '.' + extension
  old_path = file.file.path
  os.rename(file.file.path, new_path)
  new_file = DjangoFile(file.file.path)
  file.name = name + '.' + extension
  file.file.name = 'isasuk/static/storage/docs/' + str(file.id.hex) + '/' + name + '.' + extension
  file.save()
  #rename rest
  p = getFilename(old_path)
  if extension != 'pdf':
    pdf_path = os.path.join(path, name) + '.pdf'
    os.rename(p + '.pdf', pdf_path)
  if extension != 'html':
    html_path = os.path.join(path, name) + '.html'
    os.rename(p + '.html', html_path)

def convert_file(file_instance):
    filename = 'isasuk/static/storage/docs/'+ str(file_instance.id.hex) + '/' + file_instance.name
    if getExtension(file_instance.name) != 'pdf':
      while True:
          try:
              p1 = subprocess.Popen("soffice --headless --convert-to pdf 'isasuk/static/storage/docs/" + str(file_instance.id.hex) + "/" + file_instance.name + "' --outdir "  + "isasuk/static/storage/docs/" + str(file_instance.id.hex), shell=True, stdout=sys.stdout)
              p1.wait()
              break
          except:
                 print("Oops! Problem occured.  Try again...")
      iterate = True
      while iterate:
          p2 = subprocess.Popen("pdf2htmlEX " + "'isasuk/static/storage/docs/" + str(file_instance.id.hex) + "/" + ('.').join(file_instance.name.split('.')[:-1]) + ".pdf'" + " 'isasuk/static/storage/docs/" + str(file_instance.id.hex) + "/" + ('.').join(file_instance.name.split('.')[:-1]) + ".html'", shell=True, bufsize=1, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
          for line in p2.stderr:
              print(line)
              if line.startswith(b'I/O Error') or line.startswith(b'Error'):
                print("Trying again....")
              else:
                p2.wait()
                iterate = False
                break
      file_instance.save()
      return str(file_instance.id)

  def convert_to_pdf(file_name):
      path = settings.BASE_DIR + '/isasuk/media/' + file_name
      out_path = settings.BASE_DIR + '/isasuk/media/'
      while True:
        try:
            p1 = subprocess.Popen("soffice --headless --convert-to pdf " + "'" + path + "' --outdir "  + out_path, shell=True, stdout=sys.stdout)
            p1.wait()
            break
        except:
             print("Oops! Problem occured.  Try again...")
      return getFilename(file_name) + '.pdf'

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
      if getExtension(f.name) != 'pdf':
        while True:
            try:
                p1 = subprocess.Popen("soffice --headless --convert-to pdf " + "'isasuk/static/storage/docs/" + str(file_instance.id) + "/" + f.name + "' --outdir "  + "isasuk/static/storage/docs/" + str(file_instance.id), shell=True, stdout=sys.stdout)
                p1.wait()
                break
            except:
                 print("Oops! Problem occured.  Try again...")
        iterate = True
        while iterate:
            p2 = subprocess.Popen("pdf2htmlEX " + "'isasuk/static/storage/docs/" + str(file_instance.id) + "/" + ('.').join(f.name.split('.')[:-1]) + ".pdf'" + " 'isasuk/static/storage/docs/" + str(file_instance.id) + "/" + ('.').join(f.name.split('.')[:-1]) + ".html'", shell=True, bufsize=1, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
            print('here')
            for line in p2.stderr:
                print(line)
                if line.startswith(b'I/O Error') or line.startswith(b'Error'):
                  print("Trying again....")
                else:
                  p2.wait()
                  iterate = False
                  break
        file_instance.save()
        return str(file_instance.id)