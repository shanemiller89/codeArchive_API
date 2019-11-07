from django.db import models

from .coder import Coder

class Event(models.Model):

    title = models.CharField(max_length=150)
    date = models.DateField()
    location = models.CharField(max_length=150)
    description = models.TextField()
    link = models.CharField(max_length=150)
    reference = models.CharField(max_length=150)
    coder = models.ForeignKey(Coder, on_delete=models.PROTECT)

    class Meta:
        verbose_name = ("event")
        verbose_name_plural = ("events")

    def __str__(self):
        return f'{self.title}'