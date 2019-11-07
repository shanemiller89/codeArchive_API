from django.db import models
from .coder import Coder

class Article(models.Model):

    title = models.CharField(max_length=150)
    synopsis = models.TextField()
    link = models.CharField(max_length=150)
    reference = models.CharField(max_length=150)
    coder = models.ForeignKey(Coder, on_delete=models.PROTECT)

    class Meta:
        verbose_name = ("article")
        verbose_name_plural = ("articles")

    def __str__(self):
        return f'{self.title}'