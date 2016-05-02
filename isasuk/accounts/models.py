from django.db import models
from django.contrib.auth.models import User
import uuid

class Details(models.Model):
    user = models.OneToOneField(User)
    faculty = models.CharField(max_length=100, null=True, blank=True)
    title_before = models.CharField(max_length=100, null=True, blank=True)
    title_after = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100)
    start = models.CharField(max_length=100, null=True, blank=True)
    end = models.CharField(max_length=100, null=True, blank=True)
    is_student = models.BooleanField()
    is_member = models.BooleanField()
    is_chair = models.BooleanField()
    can_submit = models.BooleanField()
    archive_access = models.BooleanField()
    is_active = models.BooleanField()


class Recovery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

