# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-23 10:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0003_npro'),
    ]

    operations = [
        migrations.CreateModel(
            name='PRED',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('crc32', models.BigIntegerField(db_index=True, default=0)),
                ('vikidict_scaned', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='vocabulary.PRED')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('tree', django.db.models.manager.Manager()),
            ],
        ),
    ]
