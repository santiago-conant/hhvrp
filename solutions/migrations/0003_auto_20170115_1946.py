# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 01:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_auto_20170115_1919'),
        ('solutions', '0002_auto_20170115_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution_date', models.DateField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.Problem')),
            ],
            options={
                'ordering': ['solution_date'],
            },
        ),
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ['solution']},
        ),
        migrations.RemoveField(
            model_name='route',
            name='problem',
        ),
        migrations.AddField(
            model_name='route',
            name='solution',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='solutions.Solution'),
            preserve_default=False,
        ),
    ]