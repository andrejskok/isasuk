from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'^(?P<proposal_id>[a-z0-9\-]+)/(?P<file_id>[a-z0-9\-]+)', v.proposal_view, name='proposal_view'),
    url(r'^storage/docs/(?P<path>[A-Za-z0-9\-\/\.]+)$', v.path_view),
    url(r'^([a-z0-9\-]{0,36})$', v.document_view),
]
