import inspect
import sys

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

def get_models():
    obj_list = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        obj_list.append(obj)
    return obj_list