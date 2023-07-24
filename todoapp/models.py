from django.db import models
from django.db.models import CharField


class Task(models.Model):
    objects = None
    name: CharField = models.CharField(max_length=250)
    priority = models.IntegerField()
    date=models.DateField()

    def __str__(self):
        return self.name

