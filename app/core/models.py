from django.db import models

# Create your models here.
class Marathon(models.Model):
    status = models.BooleanField(verbose_name="status")



class ToDo(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def __str__():
        return self.title