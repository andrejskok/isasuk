from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'^download/zip/(?P<proposal_id>[-\w.]+)$', v.download_zip, name='download_zip'),
    url(r'^download/pdf/(?P<id>[-\w.]+)$', v.download_pdf, name='download_pdf'),
    url(r'^download/original/(?P<id>[-\w.]+)$', v.download_original, name='download_original'),
    url(r'^download/(?P<filename>[-\w.]+)$', v.download_file, name='download_file'),
    url(r'^print/(?P<filename>[-\w.]+)$', v.print_file),
    url(r'^show/(?P<filename>[-\w.]+)$', v.show_file),
    url(r'^file/', v.upload_file, name='jfu_upload'),
    url(r'^delete/(?P<id>\w+)$', v.delete_file, name='jfu_delete'),
    url(r'^generator/', v.generator_view, name='generator'),
    url(r'^', v.upload_view, name='upload')
]
