from django.db import models
from django.contrib.auth.models import User

class Details(models.Model):
    user = models.OneToOneField(User)
    faculty = models.CharField(max_length=100, null=True, blank=True)
    title_before = models.CharField(max_length=100, null=True, blank=True)
    title_after = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100)
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100)
    is_student = models.BooleanField()
    is_member = models.BooleanField()
    is_chair = models.BooleanField()
    can_submit = models.BooleanField()
    is_active = models.BooleanField()