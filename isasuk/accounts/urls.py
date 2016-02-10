from django.conf.urls import include, url
from django.contrib import admin
from . import views as v

urlpatterns = [
  url(r'^login/', v.login_view, name='login'),
  url(r'^logout/', v.logout_view, name='logout'),
]
