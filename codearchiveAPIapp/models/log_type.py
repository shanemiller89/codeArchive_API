from django.db import models

class LogType(models.Model):

    type = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("log type")
        verbose_name_plural = ("log types")

    def __str__(self):
        return f'{self.type}'