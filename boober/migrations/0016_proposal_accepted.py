# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-31 01:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boober', '0015_auto_20180330_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]