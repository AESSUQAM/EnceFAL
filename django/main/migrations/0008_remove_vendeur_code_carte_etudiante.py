# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-02 18:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20160611_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendeur',
            name='code_carte_etudiante',
        ),
    ]
