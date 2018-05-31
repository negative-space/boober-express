# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-30 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boober', '0006_auto_20180330_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='birthday',
        ),
        migrations.AddField(
            model_name='client',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='own_photo',
            field=models.ImageField(blank=True, null=True, upload_to='image_upload/client/own_photo', verbose_name='Selfie'),
        ),
    ]
