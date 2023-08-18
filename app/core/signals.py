from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import MainTask, SubTask

@receiver(m2m_changed, sender=MainTask.subtasks.through)
def update_main_task_status(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add' or kwargs['action'] == 'post_remove':
        subtasks_completed = instance.subtasks.filter(completed=True).count()
        if subtasks_completed == instance.subtasks.count():
            instance.completed = True
        else:
            instance.completed = False
        instance.save()


@receiver(post_save, sender=SubTask)
def update_subtask_status(sender, instance, **kwargs):
    for main_task in instance.main_tasks.all():
        update_main_task_status(sender, main_task)
