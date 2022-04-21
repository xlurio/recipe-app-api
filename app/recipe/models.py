from django.db import models
from django.conf import settings


# Create your models here.
class Tag(models.Model):
    '''Model of the recipe tags'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
