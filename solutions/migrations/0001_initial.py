# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 22:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problems', '0002_remove_problem_ncustomers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.FloatField(default=0.0)),
                ('time', models.FloatField(default=0.0)),
                ('cost', models.FloatField(default=0.0)),
                ('demand', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RouteSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.Customer')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solutions.Route')),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='route',
            field=models.ManyToManyField(through='solutions.RouteSequence', to='problems.Customer'),
        ),
    ]
