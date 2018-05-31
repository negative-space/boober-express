# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-31 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boober', '0021_driverproposalcancel_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='ridefeedback',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='image_upload/ride_feedback/picture', verbose_name='Proof of successful payment (ask first!)'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='I have seen the boobs'),
        ),
        migrations.AlterField(
            model_name='ridefeedback',
            name='feedback',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Write couple words to your client'),
        ),
        migrations.AlterField(
            model_name='ridefeedback',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='I have seen the boobs!'),
        ),
    ]
