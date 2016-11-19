# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-19 20:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookings', '0005_booking_date_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('is_confirmed', models.BooleanField(default=False)),
                ('date_confirmed', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='booking',
            name='date_confirmed',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='is_confirmed',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='slot_owner_id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='start_date',
        ),
        migrations.AddField(
            model_name='bookingdetail',
            name='booking_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.Booking'),
        ),
        migrations.AddField(
            model_name='bookingdetail',
            name='slot_owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
