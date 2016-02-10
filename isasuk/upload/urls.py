from django.conf.urls import include, url
from django.contrib import admin

from . import views as v

urlpatterns = [
    url(r'^', v.upload_view, name='upload'),
]
