# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-09-04 17:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sigad', '0006_auto_20170831_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='referenciaentredocumentos',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='sigad.ReferenciaEntreDocumentos', verbose_name='Filhos'),
        ),
        migrations.AddField(
            model_name='referenciaentredocumentos',
            name='related_classes',
            field=models.ManyToManyField(blank=True, related_name='_referenciaentredocumentos_related_classes_+', to='sigad.ReferenciaEntreDocumentos', verbose_name='Classes Relacionadas'),
        ),
        migrations.AddField(
            model_name='referenciaentredocumentos',
            name='slug',
            field=models.SlugField(default='', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='referenciaentredocumentos',
            name='titulo',
            field=models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Título'),
        ),
    ]
