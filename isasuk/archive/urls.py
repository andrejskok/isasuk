from django.conf.urls import include, url
from django.contrib import admin
from . import views as v

urlpatterns = [
  url(r'^documents/', v.archive_view, name='archive_documents'),
  url(r'^meetings/', v.meetings_view, name='archive_meetings'),
  url(r'^(?P<id>[a-z0-9\-]+)', v.archive_file_view),
]
