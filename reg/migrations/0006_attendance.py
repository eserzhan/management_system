# Generated by Django 4.1.1 on 2022-11-13 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0005_alter_subject_days'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attended', models.BooleanField()),
                ('date', models.DateTimeField()),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reg.student')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reg.subject')),
            ],
        ),
    ]