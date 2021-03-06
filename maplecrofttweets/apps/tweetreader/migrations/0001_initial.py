# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-09 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=64)),
                ('lat', models.FloatField(null=True)),
                ('lng', models.FloatField(null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddIndex(
            model_name='country',
            index=models.Index(fields=['name'], name='tweetreader_name_ab56bf_idx'),
        ),
    ]
