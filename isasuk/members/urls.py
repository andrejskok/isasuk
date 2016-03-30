from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'^verify/(?P<id>.+)', v.password_view),
    url(r'^users/', v.members_view, name='members'),
    url(r'^groups/(?P<group_name>\w{0,30})/$', v.groups_view),
    url(r'^groups/$', v.groups_view, name='groups'),
    url(r'^attendance/', v.attendance_view, name='attendance'),
    url(r'^adhoc/', v.adhoc_view, name='adhoc'),
]
