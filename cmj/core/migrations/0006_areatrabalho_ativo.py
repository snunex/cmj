# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-19 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20180216_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='areatrabalho',
            name='ativo',
            field=models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=True, verbose_name='Área de trabalho Ativa'),
        ),
    ]