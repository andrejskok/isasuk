from django.db import models
from django.contrib.auth.models import User
import uuid

def generate_filename(self, filename):
    url = "isasuk/static/storage/docs/%s/%s" % (self.id.hex, self.name)
    return url

class Proposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=50)
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=50, blank=True)

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal_id = models.CharField(max_length=50)
    path = models.CharField(max_length=50)
    file = models.FileField(upload_to=generate_filename)
    name = models.CharField(max_length=50)
    file_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    # proposal, own_material, explanatory report, UK_consideration, attachment

