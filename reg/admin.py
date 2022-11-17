from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
class UserModel(admin.ModelAdmin):
    list_display = ['username',  'status']
admin.site.register(User, UserModel)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(StudentSubject)