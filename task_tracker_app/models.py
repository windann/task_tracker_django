from django.db import models
from django.utils import timezone

class Task(models.Model):
    name_task = models.CharField(max_length=30)
    date = models.DateField(default=timezone.now)
    status = models.IntegerField(default=1)
    base_task_id = models.ForeignKey('Task', on_delete=None,null=True,blank=True)
    author = models.ForeignKey('auth.User',on_delete=None,default=None,null=True,blank=True)
    type = models.ForeignKey('Type', on_delete='null')

    def __str__(self):
        return self.name_task

class Type(models.Model):
    name_type = models.CharField(max_length=30)

    def __str__(self):
        return self.name_type


