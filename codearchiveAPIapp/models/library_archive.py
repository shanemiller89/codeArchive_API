from django.db import models

from .library import Library
from .archive import Archive

class LibraryArchive(models.Model):

    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="library")
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, related_name="archive")

    class Meta:
        verbose_name = ("library archive")
        verbose_name_plural = ("library archives")