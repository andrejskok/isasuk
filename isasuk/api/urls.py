from django.conf.urls import include, url
from django.contrib import admin
from . import views as v

urlpatterns = [
  url(r'^login', v.login),
  url(r'^logout', v.logout),
  url(r'^users', v.users),
  url(r'^meetings', v.meetings),
  url(r'^materials', v.materials),
  url(r'^material/(?P<id>[a-z0-9\-]+)', v.material),
  url(r'^file/(?P<id>[a-z0-9\-]+)', v.file),
]
