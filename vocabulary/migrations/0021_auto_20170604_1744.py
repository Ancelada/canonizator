# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0020_auto_20170604_1743'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='infn',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='infn',
            name='level',
        ),
        migrations.RemoveField(
            model_name='infn',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='infn',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='infn',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='infn',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vocabulary.INFN'),
        ),
    ]