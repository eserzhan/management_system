from django.urls import path
from .views import *

urlpatterns = [
    path('', bas, name='home'),
    path('register/', RegisterUser.as_view(), name='BaseU'),
    path('register/<str:sl_url>/', RegisterActivity.as_view(), name='act'),
    path('login/', LoginUser.as_view(), name='log'),
    path('logout/', logout_user, name='logo'),
    path('users/', ArticleListView.as_view(), name='usr'),
    path('users/<pk>/update', UserUpdateView.as_view(), name='pkk'),
    path('api/v1/teacherdetail/', TeacherList.as_view(), name='tea'),
    path('api/v1/teacherdetail/<int:nom>/', SubjectList.as_view(), name='teas'),
    path('api/v1/students/<int:nom1>/', StudentList.as_view(), name='stu'),
    path('api/v1/students/<int:nom1>/attendance', AttendanceList.as_view(), name='att')
]