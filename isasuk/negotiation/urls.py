from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'^file/', v.upload_file, name='negotiation_upload'),
    url(r'^delete/(?P<id>\w+)$', v.delete_file, name='negotiation_delete'),
    url(r'^assign/(?P<id>[a-z0-9\-]+)', v.assign_view, name='negotiation_assign'),
    url(r'^report/(?P<id>[a-z0-9\-]+)', v.report_view, name='negotiation_report'),
    url(r'^(?P<meeting_id>[a-z0-9\-]+)/(?P<file_id>[a-z0-9\-]+)', v.objections_view, name='objections'),
    url(r'^(?P<group>[a-z]+)$', v.negotiation_group_view),
    url(r'^$', v.negotiation_view, name='negotiation'),
]
