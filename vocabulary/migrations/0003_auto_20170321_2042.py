# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 17:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0002_adjs_advb_comp_conj_grnd_infn_intg_intj_latn_npro_numb_numr_pnct_prcl_pred_prep_prtf_prts_real_romn_'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CONJ',
        ),
        migrations.DeleteModel(
            name='INTJ',
        ),
        migrations.DeleteModel(
            name='NPRO',
        ),
        migrations.DeleteModel(
            name='PRCL',
        ),
        migrations.DeleteModel(
            name='PRED',
        ),
        migrations.DeleteModel(
            name='PREP',
        ),
        migrations.DeleteModel(
            name='ROMN',
        ),
        migrations.DeleteModel(
            name='UNKN',
        ),
    ]