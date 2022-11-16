from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import *


User1 = get_user_model()


class RegisterUserForm(UserCreationForm):
    roles = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    roles = [('', '-----------------')] + roles
    username = forms.CharField(label='Введите логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    job = forms.ChoiceField(label='Выберите роль', choices=roles, required=False)
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ('username', 'job', 'password1', 'password2',)


class RegisterAdminUserForm(RegisterUserForm):
    is_staff = forms.BooleanField(label='Персонал', required=False)
    is_superuser = forms.BooleanField(label='Админ', required=False)

    class Meta:
        model = User
        fields = ('username', 'job', 'password1', 'password2', 'is_staff', 'is_superuser')


class RegisterTeacherForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['user'].initial = User1.objects.latest('pk')
            self.fields['user'].disabled = True
            # self.fields['user'].initial = User.objects.latest('pk').pk

    class Meta:
        model = Teacher
        fields = ('specialization', 'education', 'user')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class RegisterStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['user'].initial = User1.objects.latest('pk')
            self.fields['user'].disabled = True
            # self.fields['user'].initial = User.objects.latest('pk').pk

    class Meta:
        model = Student
        fields = ('grade', 'user')
        widgets = {
            'grade': forms.TextInput(attrs={'class': 'form-input'}),

        }       


class RegisterSubjectForm(forms.ModelForm):
    DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)

    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'start_time': forms.TimeInput(),
            'end_time': forms.TimeInput(),
            'days': forms.CheckboxSelectMultiple()
        }       


class RegisterStudentSubjectForm(forms.ModelForm):

    class Meta:
        model = StudentSubject
        fields = '__all__'

class PickyAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        if user.status == 'unverified':
            raise ValidationError(
                "Sorry, account not verified",
                code='no_b_users',
            )
