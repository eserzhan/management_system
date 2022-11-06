# Generated by Django 4.1.1 on 2022-11-06 08:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0003_alter_subject_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='days',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=1), blank=True, size=None),
        ),
    ]
