# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-31 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boober', '0020_driverproposalcancel'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverproposalcancel',
            name='reason',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
