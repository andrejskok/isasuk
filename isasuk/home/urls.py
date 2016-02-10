from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'(?P<meeting_id>.+)', v.home_view),
    url(r'^', v.home_view, name='home'),
]
