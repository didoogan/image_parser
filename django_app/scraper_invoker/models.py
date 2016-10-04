from __future__ import unicode_literals

from django.db import models


class Query(models.Model):
    query = models.CharField(max_length=50)
    need_spiner = models.BooleanField()
    engines = models.CharField(max_length=150)
    socket_engines = models.CharField(max_length=150)


