from django.db import models
from django.contrib.auth.models import User


class Coder(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=100, blank=True)


    class Meta:
        verbose_name = ("coder")
        verbose_name_plural = ("coders")

    def __str__(self):
        return f'{self.username}'