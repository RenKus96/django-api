from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime


class Author(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, null=True, blank=True)


class Book(models.Model):
    title = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150, null=True, blank=True)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900),
                                                   MaxValueValidator(datetime.datetime.now().year)],
                                       default=datetime.datetime.now().year,
                                       )
