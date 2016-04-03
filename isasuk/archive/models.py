from django.db import models
import uuid

class Meeting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_id = models.CharField(max_length=80)
    text = models.TextField()