from django.db import models

from .log_type import LogType
from .coder import Coder

class Log(models.Model):

    title = models.CharField(max_length=100)
    reference = models.CharField(max_length=150)
    log_type = models.ForeignKey(LogType, on_delete=models.PROTECT)
    coder = models.ForeignKey(Coder, on_delete=models.PROTECT)
    archives = models.ManyToManyField("Archive", through="LogArchive")

    class Meta:
        verbose_name = ("log")
        verbose_name_plural = ("logs")

    def __str__(self):
        return f'{self.title}'