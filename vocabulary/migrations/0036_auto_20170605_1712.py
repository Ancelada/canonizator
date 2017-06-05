# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-05 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0035_auto_20170604_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='adjf',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='adjs',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advb',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comp',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='conj',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='grnd',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='infn',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='intg',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='intj',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='latn',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='noun',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='npro',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='numb',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='numr',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prcl',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pred',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prep',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prtf',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prts',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='real',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='romn',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='unkn',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='verb',
            name='vikidict_correction_tested',
            field=models.BooleanField(default=False),
        ),
    ]