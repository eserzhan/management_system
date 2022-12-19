from django import forms
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from .utils import *

class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
    
        return super(ArrayField, self).formfield(**defaults)


class User(AbstractUser):
    phone = models.CharField(max_length=12, null=True, blank=False)
    job = models.CharField(max_length=25, choices=roles, null=True, blank=True)
    status = models.CharField(default='Unverified', max_length=25, choices=statuses)

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
    name = models.CharField(max_length = 27, null = True, blank = True)
    days = ChoiceArrayField(base_field = models.CharField(max_length=20, choices=DAYS_OF_WEEK), default=list)
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
    stsu = models.ForeignKey(StudentSubject, on_delete=models.CASCADE, null = True)
    attended = models.CharField(max_length=8, choices=attendance_choices, blank=True)
    date = models.DateTimeField(default = timezone.now())
    point = models.IntegerField(
        default = 0, 
        validators = [
            MinValueValidator(0),
            MaxValueValidator(100)
            ]
        )

    def __str__(self):
        return f'{self.stsu.student.user.username} - {self.attended}'

    def get_absolute_url(self):
        return reverse("namesubj", kwargs={"pk": self.stsu})
