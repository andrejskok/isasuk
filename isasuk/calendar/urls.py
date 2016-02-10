from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'events', v.events_view, name='calendar_events'),
    url(r'^', v.calendar_view, name='calendar'),
    url(r'.*^', v.calendar_view),
]
