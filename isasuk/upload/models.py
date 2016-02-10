from django.db import models
from django.contrib.auth.models import User
import uuid

class Proposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=50)
    name = models.CharField(max_length=80)

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal_id = models.CharField(max_length=50)
    path = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    file_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    # proposal, own_material, explanatory report, UK_consideration, attachment
