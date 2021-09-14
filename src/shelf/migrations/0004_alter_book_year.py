# Generated by Django 3.2.7 on 2021-09-14 20:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelf', '0003_remove_book_authors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2021)]),
        ),
    ]
