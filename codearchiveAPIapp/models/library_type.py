from django.db import models

class LibraryType(models.Model):

    type = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("library type")
        verbose_name_plural = ("library types")

    def __str__(self):
        return f'{self.type}'