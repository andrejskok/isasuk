from django.db import models
from django.contrib.auth.models import User
import uuid

class Assignement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal_id = models.CharField(max_length=256)
    group_name = models.CharField(max_length=256)
    main_group = models.BooleanField(default=False)

class Objection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_id = models.CharField(max_length=256)
    original_text = models.CharField(max_length=5000)
    objection = models.CharField(max_length=5000)
    importance = models.CharField(max_length=256)
    user_id = models.ForeignKey(User, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal_id = models.CharField(max_length=256)
    reason = models.CharField(max_length=1500)

class History(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting_id = models.CharField(max_length=256)
    path = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    file_type = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
