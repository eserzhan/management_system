# Generated by Django 4.1.1 on 2022-11-16 08:01

from django.db import migrations, models
import reg.models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0010_remove_attendance_student_remove_attendance_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='days',
            field=reg.models.ChoiceArrayField(base_field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=20), default=list, size=None),
        ),
    ]