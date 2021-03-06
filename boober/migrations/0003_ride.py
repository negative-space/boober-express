# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-30 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boober', '0002_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('pickup_point_lat', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('pickup_point_lon', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('pickup_address', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('new', 'new'), ('waiting_proposals', 'waiting_proposals'), ('ride', 'ride'), ('failed', 'failed'), ('done', 'done')], default='', max_length=17, null=True)),
                ('pickup_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('paid', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Ride',
            },
        ),
    ]
