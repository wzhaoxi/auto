# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-08 02:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliverapi', '0005_auto_20160408_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployconfig',
            name='host_passwd',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='deployconfig',
            name='host_string',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]