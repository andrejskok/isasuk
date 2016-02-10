from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Details

class DetailsInline(admin.StackedInline):
    model = Details
    can_delete = False
    verbose_name_plural = 'details'


class UserAdmin(UserAdmin):
    inlines = (DetailsInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)