# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 14:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0016_auto_20170604_1737'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='adjs',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='adjs',
            name='level',
        ),
        migrations.RemoveField(
            model_name='adjs',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='adjs',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='adjs',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='adjs',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vocabulary.ADJS'),
        ),
    ]
