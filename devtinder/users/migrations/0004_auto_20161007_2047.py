# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20161007_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermatch',
            name='user1_has_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usermatch',
            name='user2_has_seen',
            field=models.BooleanField(default=False),
        ),
    ]
