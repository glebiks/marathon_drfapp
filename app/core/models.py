from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class FullName(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=128, blank=True)


class Status(models.Model):
    completed = models.BooleanField(default=False)


class MainTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    fullname = models.ForeignKey(FullName, default=1, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    subtasks = models.ManyToManyField('SubTask', related_name='main_tasks')


class SubTask(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
