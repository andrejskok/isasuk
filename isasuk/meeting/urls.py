from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'^add_meeting/', v.add_meeting_view, name='add_meeting'),
    url(r'^meetings/', v.meetings_view, name='meetings'),
]
