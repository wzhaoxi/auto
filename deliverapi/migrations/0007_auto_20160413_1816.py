# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-13 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliverapi', '0006_auto_20160408_1003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jenkinsconfig',
            old_name='job',
            new_name='jobName',
        ),
        migrations.AlterField(
            model_name='deployconfig',
            name='id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='jenkinsconfig',
            name='id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
    ]
