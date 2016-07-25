# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 04:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cerimonial', '0032_auto_20160725_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assuntoprocesso',
            name='created',
            field=models.DateTimeField(verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='assuntoprocesso',
            name='modified',
            field=models.DateTimeField(verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='contato',
            name='created',
            field=models.DateTimeField(verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='contato',
            name='modified',
            field=models.DateTimeField(verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='dependente',
            name='created',
            field=models.DateTimeField(verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='dependente',
            name='modified',
            field=models.DateTimeField(verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='email',
            name='created',
            field=models.DateTimeField(verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='email',
            name='modified',
            field=models.DateTimeField(verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='created',
            field=models.DateTimeField(verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='modified',
            field=models.DateTimeField(verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='filiacaopartidaria',
            name='created',
            field=models.DateTimeField(verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='filiacaopartidaria',
            name='modified',
            field=models.DateTimeField(verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='localtrabalho',
            name='created',
            field=models.DateTimeField(verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='localtrabalho',
            name='modified',
            field=models.DateTimeField(verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='processo',
            name='created',
            field=models.DateTimeField(verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='processo',
            name='modified',
            field=models.DateTimeField(verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='telefone',
            name='created',
            field=models.DateTimeField(verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='telefone',
            name='modified',
            field=models.DateTimeField(verbose_name='modified'),
        ),
    ]
