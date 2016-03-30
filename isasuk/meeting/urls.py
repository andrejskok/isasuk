from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'^meeting/(?P<id>[\w]+)', v.meeting_view, name='meeting'),
    url(r'^my_meetings/', v.my_meetings_view, name='my_meetings'),
    url(r'^add_meeting/', v.add_meeting_view, name='add_meeting'),
    url(r'^upload_invitation/(?P<id>[\w]+)$', v.upload_invitation_view, name='upload_invitation'),
    url(r'^edit_meeting/(?P<id>[\w]+)$', v.edit_meeting_view, name='edit_meeting'),
    url(r'^save/', v.save_meeting_program, name='save_meeting'),
    url(r'^file/', v.upload_file, name='upload_invitation_file'),
    url(r'^conclusion_material/delete/(?P<id>[\w]+)$', v.delete_conclusion_material, name='conclusion_material_delete'),
    url(r'^conclusion_material/', v.upload_conclusion_to_material, name='upload_conclusion_to_material'),
    url(r'^conclusion/delete/(?P<id>[\w]+)$', v.delete_conclusion_file, name='conclusion_delete'),
    url(r'^conclusion/', v.upload_conclusion_file, name='upload_conclusion_file'),
    url(r'^close/(?P<id>[\w]+)$', v.close_meeting_view, name='close_meeting'),
    url(r'^invitation/delete/(?P<id>[\w]+)$', v.delete_file, name='invitation_delete'),
]
