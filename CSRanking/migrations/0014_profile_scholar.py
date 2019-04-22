# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-04-21 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CSRanking', '0013_auto_20190421_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='scholar',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CSRanking.Scholar'),
        ),
    ]
