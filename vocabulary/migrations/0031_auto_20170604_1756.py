# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0030_auto_20170604_1755'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='numb',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='numb',
            name='level',
        ),
        migrations.RemoveField(
            model_name='numb',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='numb',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='numb',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='latn',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vocabulary.LATN'),
        ),
        migrations.AlterField(
            model_name='numb',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vocabulary.NUMB'),
        ),
    ]