from django.db import models
from django.contrib.auth.models import User

class Details(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(max_length=100)
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100)
    is_student = models.BooleanField()
    is_member = models.BooleanField()
    is_chair = models.BooleanField()
    can_submit = models.BooleanField()