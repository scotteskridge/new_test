# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 20:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('start_date', models.DateField(blank=True)),
                ('start_time', models.TimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_created_by', to='login.User')),
            ],
        ),
    ]
