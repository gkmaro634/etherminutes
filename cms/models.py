from django.db import models

# Create your models here.


class Minutes(models.Model):
    """minutes"""
    name = models.CharField('Minutes Title', max_length=255)
    minutes_url = models.CharField('Minutes URL', max_length=255, blank=True)

    def __str__(self):
        return self.name
