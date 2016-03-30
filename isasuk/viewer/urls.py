from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'^view/(?P<file_id>[a-z0-9\-]+)', v.view_document, name='view_document'),
    url(r'^file/(?P<file_id>[a-z0-9\-]+)', v.file_view, name='file_view'),
    url(r'^(?P<proposal_id>[a-z0-9\-]+)/(?P<file_id>[a-z0-9\-]+)', v.proposal_view, name='proposal_view'),
    url(r'^(?P<proposal_id>[a-z0-9\-]+)/', v.proposal_view, name='proposal_view_no_id'),
]
