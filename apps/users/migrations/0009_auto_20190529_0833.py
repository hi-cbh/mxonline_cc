# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-05-29 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190526_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='code',
            field=models.CharField(max_length=35, verbose_name='验证码'),
        ),
    ]
