from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^accounts/', include('isasuk.accounts.urls')),
    url(r'^home/', include('isasuk.home.urls')),
    url(r'^upload/', include('isasuk.upload.urls')),
    url(r'^objections/', include('isasuk.objections.urls')),
    url(r'^negotiation/', include('isasuk.negotiation.urls')),
    url(r'^meeting/', include('isasuk.meeting.urls')),
    url(r'^viewer/', include('isasuk.viewer.urls')),
    url(r'^calendar/', include('isasuk.calendar.urls')),
    url(r'^isasuk/', include('isasuk.viewer.urls')),
    url(r'^members/', include('isasuk.members.urls')),
    url(r'^archive/', include('isasuk.archive.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('isasuk.home.urls')),
    url(r'^.*$', include('isasuk.home.urls')),
]

