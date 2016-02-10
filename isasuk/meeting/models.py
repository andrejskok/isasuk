from django.db import models
import uuid

class Meeting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80)
    date = models.DateTimeField()
    group = models.CharField(max_length=80)
    invitation = models.CharField(max_length=80)
