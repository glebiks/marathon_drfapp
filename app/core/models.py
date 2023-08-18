from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()  


class Status(models.Model):
    completed = models.BooleanField(default=False)


class MainTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    completed = models.BooleanField(default=False)
    subtasks = models.ManyToManyField('SubTask', related_name='main_tasks')


class SubTask(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)


