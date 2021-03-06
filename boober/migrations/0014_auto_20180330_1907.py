# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-31 00:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boober', '0013_merge_20180330_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalPickup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('consent', models.BooleanField(default=False, verbose_name="I confirm I am at least 18 years old, and I'm not against to see naked boobs after the ride.")),
                ('proposal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pickup', to='boober.Proposal')),
            ],
            options={
                'verbose_name': 'Proposal pickup',
            },
        ),
        migrations.CreateModel(
            name='RideFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('feedback', models.TextField(blank=True, default='', null=True)),
            ],
            options={
                'verbose_name': 'Ride feedback',
            },
        ),
        migrations.CreateModel(
            name='RideFinish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Ride finish',
            },
        ),
        migrations.AlterField(
            model_name='proposalaccept',
            name='proposal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accept', to='boober.Proposal'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='status',
            field=models.CharField(blank=True, choices=[('waiting_proposals', 'waiting_proposals'), ('client_accepted', 'client_accepted'), ('ride', 'ride'), ('canceled', 'canceled'), ('done', 'done')], default='', max_length=17, null=True),
        ),
        migrations.AddField(
            model_name='ridefinish',
            name='ride',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='finish', to='boober.Ride'),
        ),
        migrations.AddField(
            model_name='ridefeedback',
            name='ride',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='boober.Ride'),
        ),
    ]
