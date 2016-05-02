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
    state = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    category = models.CharField(max_length=256, blank=True)

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal_id = models.CharField(max_length=256)
    path = models.CharField(max_length=256)
    file = models.FileField(upload_to=generate_filename, max_length=1000)
    name = models.CharField(max_length=256)
    file_type = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
    # proposal, own_material, explanatory report, UK_consideration, attachment

