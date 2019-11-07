from django.db import models

class RecordType(models.Model):

    type = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("record type")
        verbose_name_plural = ("record types")

    def __str__(self):
        return f'{self.type}'