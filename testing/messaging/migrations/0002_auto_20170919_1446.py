# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-19 09:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smstracking',
            old_name='number',
            new_name='phone',
        ),
    ]
