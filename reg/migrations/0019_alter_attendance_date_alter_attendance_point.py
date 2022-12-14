# Generated by Django 4.1.1 on 2022-12-10 18:47

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0018_attendance_point_alter_attendance_date_delete_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 10, 18, 47, 5, 797258, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='point',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
