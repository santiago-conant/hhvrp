# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 01:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_problem_depot'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='problem',
            options={'ordering': ['name']},
        ),
    ]