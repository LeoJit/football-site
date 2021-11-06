import inspect
import sys

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from django.contrib.postgres.fields import JSONField

def get_models():
    obj_list = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        obj_list.append(obj)
    return obj_list

class Fixtures(models.Model):
    league= models.CharField(max_length=200, null=False)
    matches= JSONField()

class Players(models.Model):
    name = models.CharField(max_length=200, null=False)
    link = models.CharField(max_length=500, null=False)
    club = models.CharField(max_length=200, null=False)
    nationality = models.CharField(max_length=200, null=False)
    market_value = models.CharField(max_length=200, null=False)
    height = models.CharField(max_length=200, null=False)
    logo = models.CharField(max_length=200, null=False)
    picture = models.CharField(max_length=200, null=False)
    infos = JSONField()
    stats = JSONField()

