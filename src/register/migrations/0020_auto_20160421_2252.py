# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-21 22:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0019_auto_20160414_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apostillerequest',
            name='status',
            field=models.CharField(choices=[('p', 'Pending'), ('a', 'Approved'), ('r', 'Rejected')], default='p', max_length=1),
        ),
    ]
