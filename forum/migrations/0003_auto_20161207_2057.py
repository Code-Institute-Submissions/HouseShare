# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 20:57
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_thread_num_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='description',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]