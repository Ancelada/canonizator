# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_normalizepublicationerror_normalizepublicationstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='copypublication',
            name='author',
            field=models.CharField(blank=True, db_index=True, max_length=512, null=True),
        ),
    ]
