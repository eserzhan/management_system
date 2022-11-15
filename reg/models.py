from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django import forms


class ChoiceArrayField(ArrayField):
    
    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
    
        return super(ArrayField, self).formfield(**defaults)


class User(AbstractUser):
    statuses = [
        ('Unverified', 'unverified'),
        ('Verified', 'verified'),
        ('Deactivated', 'deactivated'),
    ]
    roles = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
]
    phone = models.IntegerField(null=True, blank=True)
    job = models.CharField(max_length=25, choices=roles, null=True, blank=True)
    status = models.CharField(default='unverified', max_length=25, choices=statuses)

    def __str__(self):
        return f'{self.username} - {self.status}'

    def get_absolute_url(self):
        return reverse("pkk", kwargs={"pk": self.pk})


class Teacher(models.Model):
    specialization = models.CharField(max_length = 27, null = True, blank = True)
    education = models.CharField(max_length = 27, null = True, blank = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f'{self.user.username} - {self.specialization}'

class Student(models.Model):
    grade = models.IntegerField(null = True, blank = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f'{self.user.username} - {self.grade}'

class Subject(models.Model):
    DAYS_OF_WEEK = (
    ('0', 'Monday'),
    ('1', 'Tuesday'),
    ('2', 'Wednesday'),
    ('3', 'Thursday'),
    ('4', 'Friday'),
    ('5', 'Saturday'),
    ('6', 'Sunday'),
)

    name = models.CharField(max_length = 27, null = True, blank = True)
    days = ChoiceArrayField(base_field = models.CharField(max_length=1, choices=DAYS_OF_WEEK), default=list)
    time = ArrayField(base_field = models.CharField(max_length=255), default=list)
    cabinet = models.IntegerField(null = True, blank = True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f'{self.name} - {self.cabinet}'

class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null = True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f'{self.student.user.username} - {self.subject.name}'

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null = True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null = True)
    attended = models.BooleanField()
    date = models.DateTimeField()
    
    def __str__(self):
        return f'{self.student.user.username} - {self.attended}'