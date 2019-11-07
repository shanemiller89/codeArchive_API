import os
import uuid

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .library_type import LibraryType
from .coder import Coder


class Library(models.Model):

    title = models.CharField(max_length=50)
    link = models.CharField(max_length=150)
    image = models.CharField(blank=True, max_length=150)
    image_title = models.CharField(max_length=100)
    library_type = models.ForeignKey(LibraryType, on_delete=models.PROTECT)
    parent_library = models.ForeignKey('self',null=True, on_delete=models.CASCADE, related_name="sub_libraries")
    archives = models.ManyToManyField("Archive", through="LibraryArchive")
    coder = models.ForeignKey(Coder, on_delete=models.PROTECT)

    class Meta:
        ordering = ["title"]
        verbose_name = ("library")
        verbose_name_plural = ("libraries")

    def __str__(self):
        return f'{self.title}'