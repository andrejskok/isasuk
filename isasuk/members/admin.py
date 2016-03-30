from django.contrib import admin
from .models import Group, AdhocGroup, Attendance

admin.site.register(Group)
admin.site.register(AdhocGroup)
admin.site.register(Attendance)