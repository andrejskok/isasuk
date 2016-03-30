from django.db import models
import uuid
from ..upload.models import Proposal, File, generate_filename

class Meeting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80)
    date = models.DateTimeField()
    group = models.CharField(max_length=80)
    invitation = models.ForeignKey(File, blank=True, null=True, related_name='meeting_invitation')
    program = models.ForeignKey(File, blank=True, null=True, related_name='meeting_program')
    conclusion = models.ForeignKey(File, blank=True, null=True, related_name='meeting_conclusion')
    closed = models.BooleanField(default=False)
    state = models.CharField(max_length=20)

class MeetingsToMaterials(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting = models.ForeignKey(Meeting)
    proposal = models.ForeignKey(Proposal)
    title = models.ForeignKey(File, blank=True, null=True)
    conclusion = models.ForeignKey(File, blank=True, null=True, related_name='m2m_conclusion')
    name = models.CharField(max_length=80)
    order = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

