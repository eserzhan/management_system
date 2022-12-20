from django import forms
from django.forms import modelformset_factory
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .utils import *
from .models import *


User1 = get_user_model()


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Surname', widget=forms.TextInput(attrs={'class': 'form-input'}))
    roles = [('', '-----------------')] + roles
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    job = forms.ChoiceField(label='Role', choices=roles, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'job', 'password1', 'password2', 'phone')


class RegisterAdminUserForm(RegisterUserForm):
    is_staff = forms.BooleanField(label='Staff', required=False)
    is_superuser = forms.BooleanField(label='Admin', required=False)

    class Meta:
        model = User
        fields = ('username', 'job', 'password1', 'password2', 'is_staff', 'is_superuser', 'status')


class RegisterTeacherForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
            self.request = kwargs.pop("request")
            super().__init__(*args, **kwargs)
            self.fields['user'].initial = User1.objects.latest('pk')
            self.fields['user'].disabled = True

    class Meta:
        model = Teacher
        fields = ('specialization', 'education', 'user')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class RegisterStudentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = User1.objects.latest('pk')
        self.fields['user'].disabled = True

    class Meta:
        model = Student
        fields = ('grade', 'user')
        widgets = {
            'grade': forms.TextInput(attrs={'class': 'form-input'})
        }       


class RegisterSubjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        print(self.request)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'days': forms.CheckboxSelectMultiple()
        }       

class RegisterSelfSubjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ('name', 'days', 'time','cabinet')
        widgets = {
            'days': forms.CheckboxSelectMultiple()
        }       


class RegisterStudentSubjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    class Meta:
        model = StudentSubject
        fields = '__all__'


class PickyAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        print(user.status)
        if user.status == 'Unverified':
            raise ValidationError(
                "Account not verified. Contact admin.",
                code='no_b_users',
            )
            

class Attendanceform(forms.ModelForm):

    def __init__(self, *args, **kwargs):
            self.request = kwargs.pop("request")
            super().__init__(*args, **kwargs)
            self.fields['stsu'].initial = StudentSubject.objects.get(
                    Q(subject__name=self.request['sbj_name']) & Q(student__user__username=self.request['st_name'])  
                )
            self.fields['stsu'].disabled = True
            
    class Meta:
        model = Attendance
        fields = ('stsu', 'attended', 'point')


class AttendanceAllform(forms.ModelForm):

    def __init__(self, *args, **kwargs):
            self.__class__.request = kwargs.pop("request")
            super().__init__(*args, **kwargs)

    class Meta:
        model = Attendance
        fields = ('stsu', 'attended', 'point')
