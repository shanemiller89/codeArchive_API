from django.db import models

class ResourceType(models.Model):

    type = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("resource type")
        verbose_name_plural = ("resource types")

    def __str__(self):
        return f'{self.type}'