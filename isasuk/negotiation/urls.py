from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'^$', v.negotiation_view, name='negotiation'),
    url(r'^assign/(?P<id>[a-z0-9\-]+)', v.assign_view, name='negotiation_assign'),
    url(r'^report/(?P<id>[a-z0-9\-]+)', v.report_view, name='negotiation_report'),
    url(r'^(?P<group>[a-z]+)$', v.negotiation_group_view),
    url(r'^(?P<group>[a-z]+)/(?P<proposal_id>[a-z0-9\-]+)/(?P<file_id>[a-z0-9\-]+)', v.objections_view, name='objections'),
    url(r'^(?P<group>[a-z]+)/(?P<proposal_id>[a-z0-9\-]+)', v.objections_redirect_view, ),
]
