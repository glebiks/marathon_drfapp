from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()  


class Status(models.Model):
    completed = models.BooleanField(default=False)


class GlobalTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    completed = models.BooleanField(default=False)


class SubTask(models.Model):
    relate_to = models.ForeignKey(GlobalTask, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)


