# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 00:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_auto_20170203_2134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['-timestamp', 'content']},
        ),
    ]
