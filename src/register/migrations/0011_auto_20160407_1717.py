# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-07 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0010_auto_20160318_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='signer',
        ),
        migrations.AddField(
            model_name='document',
            name='signer_name',
            field=models.CharField(default='No provided', max_length=150),
            preserve_default=False,
        ),
    ]
