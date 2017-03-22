# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manager', '0002_auto_20170212_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crawler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=512, null=True)),
                ('file_name', models.CharField(blank=True, max_length=512, null=True)),
                ('imported', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=512, null=True)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(db_index=True)),
                ('url', models.URLField()),
                ('crawler', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.Crawler')),
            ],
        ),
    ]