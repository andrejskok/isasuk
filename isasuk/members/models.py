from django.db import models
from django.contrib.auth.models import User
import uuid

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=50)
    member = models.ForeignKey(User)
    is_chair = models.BooleanField()

class AdhocGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=50)
    member = models.ForeignKey(User)
