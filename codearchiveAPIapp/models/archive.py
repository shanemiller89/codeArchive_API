from django.db import models

from .library import Library
from .log import Log

class Archive(models.Model):

    title = models.CharField(max_length=100)
    link = models.CharField(max_length=150)
    libraries = models.ManyToManyField(Library)
    logs = models.ManyToManyField(Log)

    class Meta:
        ordering = ["title"]
        verbose_name = ("archive")
        verbose_name_plural = ("archives")

    def __str__(self):
        return f'{self.title}'