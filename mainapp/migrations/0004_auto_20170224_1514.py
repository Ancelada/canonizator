# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_remove_publicationcopy_publication_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationNormalized',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=512, null=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='publicationcopy',
            name='title',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
