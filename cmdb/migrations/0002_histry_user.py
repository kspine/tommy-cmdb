# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-26 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='histry',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Users', verbose_name='用户'),
            preserve_default=False,
        ),
    ]
