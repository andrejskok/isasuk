from django.conf.urls import include, url
from django.contrib import admin
from . import views as v

urlpatterns = [
  url(r'^api', v.archive_api),
  url(r'^(?P<id>[a-z0-9\-]+)', v.archive_file_view),
  url(r'^', v.archive_view, name='archive'),
]
