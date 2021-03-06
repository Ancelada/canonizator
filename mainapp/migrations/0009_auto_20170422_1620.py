# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-22 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20170421_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='normalizepublication',
            name='author',
            field=models.CharField(blank=True, db_index=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='normalizepublication',
            name='crawler_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='normalizepublication',
            name='name',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='normalizepublication',
            name='name_cyrillic',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='normalizepublication',
            name='pubdate',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
