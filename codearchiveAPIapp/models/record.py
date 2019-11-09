import os
import uuid

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .record_type import RecordType
from .archive import Archive


class Record(models.Model):

    title = models.CharField(max_length=50)
    text = models.TextField()
    image = models.CharField(blank=True, max_length=150)
    image_title = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=50, blank=True)
    order = models.IntegerField()
    record_type = models.ForeignKey(RecordType, on_delete=models.PROTECT)
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, related_name="records")

    class Meta:
        ordering = ["order"]
        verbose_name = ("record")
        verbose_name_plural = ("records")

    def __str__(self):
        return f'{self.title}'