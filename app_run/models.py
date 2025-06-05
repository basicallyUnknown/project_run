from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


# Create your models here.

class Run(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    comment = models.TextField()
    athlete = models.ForeignKey(User, on_delete=CASCADE)