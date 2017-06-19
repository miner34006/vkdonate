# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-17 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_title', models.CharField(max_length=100)),
                ('article_text', models.CharField(max_length=1000)),
                ('article_datePub', models.DateTimeField()),
                ('article_image', models.ImageField(upload_to='images/')),
            ],
            options={
                'db_table': 'articles',
            },
        ),
    ]
