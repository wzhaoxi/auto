# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-08 02:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliverapi', '0004_auto_20160407_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jenkinsconfig',
            name='password',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='jenkinsconfig',
            name='user',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
