# Generated by Django 4.1.1 on 2022-11-13 15:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0006_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='start_time',
        ),
        migrations.AddField(
            model_name='subject',
            name='time',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=list, size=None),
        ),
    ]
