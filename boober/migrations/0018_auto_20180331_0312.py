# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-31 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boober', '0017_auto_20180331_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
