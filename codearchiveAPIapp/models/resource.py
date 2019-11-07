from django.db import models

from .resource_type import ResourceType
from .archive import Archive

class Resource(models.Model):

    title = models.CharField(max_length=100)
    link = models.CharField(max_length=150)
    description = models.TextField()
    resource_type = models.ForeignKey(ResourceType, on_delete=models.PROTECT)
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, related_name="resources")

    class Meta:
        verbose_name = ("resource")
        verbose_name_plural = ("resources")

    def __str__(self):
        return f'{self.title}'