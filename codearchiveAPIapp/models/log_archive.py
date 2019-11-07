from django.db import models

from .log import Log
from .archive import Archive

class LogArchive(models.Model):

    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("log archive")
        verbose_name_plural = ("log archives")