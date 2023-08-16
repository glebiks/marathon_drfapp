from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)


class ToDo(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    # def __str__():
    #     return self.title

# class GlobalTask(models.Model):
#     title = models.CharField(max_length=100, blank=False)
#     user = models.ForeignKey(User, verbose_name='assign_to', on_delete=models.CASCADE)