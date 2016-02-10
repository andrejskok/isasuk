from django.conf.urls import include, url
from django.contrib import admin
from . import views as v

urlpatterns = [
  url(r'^(?P<id>[a-z0-9\-]+)', v.archive_view),
]
