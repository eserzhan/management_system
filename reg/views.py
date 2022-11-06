from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from reg.forms import *
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import logout


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


    