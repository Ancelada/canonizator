# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 09:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_publicationcopy_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicationcopy',
            name='Publication_id',
        ),
    ]
