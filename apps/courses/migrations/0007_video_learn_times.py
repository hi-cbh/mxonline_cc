# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-06-24 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='时长（分钟数）'),
        ),
    ]
