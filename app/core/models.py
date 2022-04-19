import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings

# Create your models here.


class Ingredient(models.Model):
    """Ingredient model"""
    name = models.CharField(max_length=225)
    recipe = models.ForeignKey(
        'Recipe',
        related_name='ingredients',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe model"""
    name = models.CharField(max_length=225)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
