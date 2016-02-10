from django.contrib import admin
from .models import Group, AdhocGroup

admin.site.register(Group)
admin.site.register(AdhocGroup)