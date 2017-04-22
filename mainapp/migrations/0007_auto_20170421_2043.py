# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-21 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_pubcompareerror_pubcomparestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='copypublication',
            name='crawler_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='copypublication',
            name='name_cyrillic',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
