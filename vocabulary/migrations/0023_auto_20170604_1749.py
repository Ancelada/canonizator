# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0022_auto_20170604_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prtf',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vocabulary.PRTF'),
        ),
    ]
