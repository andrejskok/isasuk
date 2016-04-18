from django.db import models
from django.contrib.auth.models import User
from ..meeting.models import Meeting
import uuid

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=50)
    member = models.ForeignKey(User)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    is_chair = models.BooleanField()

class AdhocGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=50)
    member = models.ForeignKey(User)

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    meeting = models.ForeignKey(Meeting)
    state = models.CharField(max_length=50, blank=True)

