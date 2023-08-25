from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class FullName(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=128, blank=True)


class Status(models.Model):
    ready = models.BooleanField(default=False)


class MainTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    fullname = models.ForeignKey(FullName, default=1, on_delete=models.CASCADE)
    completed_tasks_num = models.IntegerField(blank=True, default=0)
    all_tasks_num = models.IntegerField(blank=True, default=0)
    phone = models.CharField(max_length=16, default="+79999999999")
    ready = models.BooleanField(default=False)


class SubTask(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    ready = models.BooleanField(default=False)
    maintask = models.ForeignKey(MainTask, on_delete=models.CASCADE)
