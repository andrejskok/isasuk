from django.db import models
from ..upload.models import File
import uuid

class ArchiveDocs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(File)
    text = models.TextField()
