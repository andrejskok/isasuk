from django.contrib import admin
from .models import Meeting, MeetingsToMaterials, Invited

admin.site.register(Invited)
admin.site.register(Meeting)
admin.site.register(MeetingsToMaterials)
