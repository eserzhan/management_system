from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from reg.forms import *
from rest_framework import generics
from .serializers import *
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
class RegisterUser(CreateView):
    form_class = None
    template_name = 'reg/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_success_url(self):
        return f'{self.object.job}/'

    def setup(self, request, *args, **kwargs):
        if request.user.is_staff and request.user.is_superuser:
            self.__class__.form_class = RegisterAdminUserForm
        else:
            self.__class__.form_class = RegisterUserForm

        return super().setup(request, *args, **kwargs)

    
class RegisterActivity(CreateView):
    form_class = None
    template_name = 'reg/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def setup(self, request, *args, **kwargs):
        if kwargs['sl_url'] == 'student':
            self.__class__.form_class = RegisterStudentForm
        elif kwargs['sl_url'] == 'teacher':
            self.__class__.form_class = RegisterTeacherForm
        elif kwargs['sl_url'] == 'teacher-subject':
            self.__class__.form_class = RegisterSubjectForm
        else:
            self.__class__.form_class = RegisterStudentSubjectForm
        return super().setup(request, *args, **kwargs)


class ArticleListView(ListView):
    model = User
    paginate_by = 100  # if pagination is desired
    template_name = 'reg/articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserUpdateView(UpdateView):
    model = User
    fields = ['status']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('usr')
    context_object_name = 'use'

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'reg/login.html'
    authentication_form = PickyAuthenticationForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def post(self, request, *args: str, **kwargs) -> HttpResponse:
        return super().post(request, *args, **kwargs)


def bas(request):
  
    if request.user.__str__() != 'AnonymousUser':
        if request.user.status == 'Deactivated':
            return HttpResponseForbidden()
    
    return render(request, 'reg/base.html')


def logout_user(request):
    logout(request)
    return redirect('log')


class TeacherAPIView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class TeacherList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile_list.html'

    def get(self, request, *args, **kwargs):
        queryset = Teacher.objects.all()
        return Response({'teachers': queryset})



class StudentList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = None
    temp = None
    new = None 
    def get(self, request, *args, **kwargs):
        queryset = self.__class__.temp
        return Response({self.__class__.new: queryset})

    def setup(self, request, *args, **kwargs):
        if len(kwargs) == 1:
            self.__class__.template_name = 'subjects_list.html'
            self.__class__.temp = Subject.objects.filter(teacher__user__username = kwargs['teachername'])
            self.__class__.new = 'subjects'
        elif len(kwargs) == 2:
            self.__class__.template_name = 'students_list.html'
            self.__class__.temp = StudentSubject.objects.filter(subject__name = kwargs['subj'])
            self.__class__.new = 'students'
        else:
            self.__class__.template_name = 'attendance_list.html'
            self.__class__.temp = Attendance.objects.filter(Q(stsu__student__user__username=kwargs['stud']) & Q(stsu__subject__name=kwargs['subj']))
            self.__class__.new = 'attendance'
        return super().setup(request, *args, **kwargs)
    

class SubjectList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'subject.html'
    

    def get(self, request, *args, **kwargs):
        queryset = Subject.objects.all()
        return Response({'subjects': queryset})

class Student(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'students.html'
    

    def get(self, request, *args, **kwargs):
        print(kwargs)
        queryset = StudentSubject.objects.filter(subject__name= kwargs['subjname'])
        return Response({'students': queryset})

class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.kwargs
        return kwargs
class AttendanceCreate(PassRequestToFormViewMixin, CreateView):
    form_class = Attendanceform
    template_name = 'reg/att_update_form.html'
    success_url = reverse_lazy('home')
