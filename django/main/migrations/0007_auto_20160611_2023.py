# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-12 00:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_vendeur_code_carte_etudiante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendeur',
            name='code_carte_etudiante',
            field=models.IntegerField(blank=True, help_text=b'Scannez la carte \xc3\xa9tudiante', null=True, verbose_name=b'Code carte \xc3\xa9tudiante'),
        ),
    ]
