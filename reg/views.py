from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from django.db.models import Q
from django.forms import modelformset_factory
from rest_framework import generics

from reg.forms import *
from .serializers import *


class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'

    def get(self, request):
        employees = User.objects.all()
        return render(request, self.template, {'users': employees})


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.kwargs
        return kwargs


class AttendanceForAll(PassRequestToFormViewMixin, CreateView):
    form_class = AttendanceAllform
    template_name = 'forall.html'
    success_url = reverse_lazy('index')
    temp = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.__class__.AttendanceFormSet(queryset=Attendance.objects.none(),initial=self.temp )
        return context

    def post(self, request, *args, **kwargs):
        formset = self.__class__.AttendanceFormSet(request.POST)
        print(formset)
        if formset.is_valid() :
            return self.form_valid(formset)
        
    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        return HttpResponseRedirect(self.__class__.success_url)

    def setup(self, request, *args, **kwargs):
        self.__class__.AttendanceFormSet = modelformset_factory(Attendance, fields =('stsu', 'attended', 'point'),extra=len(StudentSubject.objects.filter(subject__name=kwargs['sbj_name'])))
        self.__class__.temp = [{'stsu': x, 'attended':'absent', 'point': 0} for x in StudentSubject.objects.filter(subject__name=kwargs['sbj_name'])]
        return super().setup(request, *args, **kwargs)


class RegisterUser(CreateView):
    form_class = None
    template_name = 'register.html'

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

    
class RegisterActivity(PassRequestToFormViewMixin, CreateView):
    form_class = None
    template_name = 'register.html'
    success_url = reverse_lazy('index')

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


class RegisterSelfSubject(PassRequestToFormViewMixin, CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('index')
    form_class = RegisterSelfSubjectForm

    def form_valid(self, form):
        user = self.request.user.pk
        teacher_n = Teacher.objects.get(user_id = user)
        form.instance.teacher_id = teacher_n.pk

        return super().form_valid(form)
    
    
class TeacherAPIView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class UserListView(ListView):
    model = User
    paginate_by = 100  
    template_name = 'users_list.html'


class UserUpdateView(UpdateView):
    model = User
    fields = ['status']
    #template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')
    context_object_name = 'use'
    template_name = 'user_update_form.html'

class AttendanceUpdateView(UpdateView):
    model = Attendance
    fields = ['attended', 'point']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')
    context_object_name = 'use'


class LoginUser(UserPassesTestMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    authentication_form = PickyAuthenticationForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return reverse_lazy('index')

    def test_func(self):
        return self.request.user.__str__() == 'AnonymousUser'
        

def logout_user(request):
    logout(request)
    return redirect('log')


class TeacherList(UserPassesTestMixin, ListView):
    template_name = 'teachers_list.html'
    context_object_name = 'teachers'

    def get(self, request, *args, **kwargs):
        self.__class__.queryset = Teacher.objects.all()
        return super().get(request, *args, **kwargs)
    
    def test_func(self):
        return  self.request.user.is_staff


class SubjectList(ListView):
    template_name = 'subjects_list.html'
    context_object_name = 'subjects'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff and request.user.is_superuser:
            if len(kwargs) == 0:
                self.__class__.queryset = Subject.objects.all()

            else:
                user = User.objects.get(username=kwargs['teachername']).pk
                teacher_n = Teacher.objects.get(user_id = user)
                self.__class__.queryset = Subject.objects.filter(teacher_id = teacher_n.pk)
            
        elif request.user.job == 'teacher':
            user = request.user.pk
            teacher_n = Teacher.objects.get(user_id = user)
            self.__class__.queryset = Subject.objects.filter(teacher_id = teacher_n.pk)
        
        elif request.user.job == 'student':
            self.__class__.queryset = StudentSubject.objects.filter(student__user__username=kwargs['st_name'])
            
        return super().get(request, *args, **kwargs)
    
    # def test_func(self):
    #     return (self.request.user.job == 'teacher' and reverse('namesubj') in self.request.path) or (reverse('tea') in self.request.path and self.request.user.is_staff) or \
    #         (self.request.user.job == 'student' and reverse('mysubj', kwargs={'st_name':self.kwargs.get('st_name', None)}) in self.request.path)


class AllSubjectList(ListView):
    template_name = 'subjects_list.html'
    context_object_name = 'subjects'

    def get(self, request, *args, **kwargs):
        self.__class__.queryset = Subject.objects.all()
     
        return super().get(request, *args, **kwargs)


class StudentList(ListView):
    template_name = 'students.html'
    context_object_name = 'students'

    def get(self, request, *args, **kwargs):
        self.__class__.queryset = StudentSubject.objects.filter(subject__name = kwargs['sbj_name'])
     
        return super().get(request, *args, **kwargs)

    # def test_func(self):
    #     return (self.request.user.job == 'teacher' and reverse('namestu', kwargs={'sbj_name': self.kwargs['sbj_name']}) in self.request.path) \
    #          or \
    #             (reverse('stu', kwargs={'teachername': self.kwargs.get('teachername', None),'sbj_name': self.kwargs['sbj_name']}) in self.request.path \
    #             and self.request.user.is_staff)


class AllStudentsList(ListView):
    template_name = 'students_list.html'
    context_object_name = 'students'

    def get(self, request, *args, **kwargs):
        self.__class__.queryset = Student.objects.all()
     
        return super().get(request, *args, **kwargs)


class AttendanceView(ListView):
    template_name = 'attendance_list.html'
    context_object_name = 'attendances'
   
    def get(self, request, *args, **kwargs) :
        self.__class__.queryset = Attendance.objects.filter(Q(stsu__student__user__username=kwargs['st_name']) & Q(stsu__subject__name=kwargs['sbj_name']))
        return super().get(request, *args, **kwargs)
