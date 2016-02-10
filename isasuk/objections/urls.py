from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'^$', v.objections_view),
    url(r'^([a-z0-9\-]{36})$', v.document_view),
]
