from django.urls import path
from .views import *


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('register/<int:num>/', RegisterSelfSubject.as_view(), name='selfsubj'),
    path('register/<str:sl_url>/', RegisterActivity.as_view(), name='act'),
    
    path('<str:st_name>/mysubjects/', SubjectList.as_view(), name='mysubj'),
    path('<str:st_name>/mysubjects/<str:sbj_name>/attendance', AttendanceView.as_view(), name='mysubjdet'),

    path('login/', LoginUser.as_view(), name='log'),
    path('logout/', logout_user, name='logo'),

    path('users/', UserListView.as_view(), name='users'),
    path('users/<pk>/update', UserUpdateView.as_view(), name='pkk'),

    path('students/', AllStudentsList.as_view()),

    path('teachers/', TeacherList.as_view(), name='teachers'),
    path('teacher/<str:teachername>/subject/', SubjectList.as_view(), name='teacher_subject'),
    path('teacher/<str:teachername>/subject/<str:sbj_name>/', StudentList.as_view(), name='stu'),
    path('teacher/<str:teachername>/subject/<str:sbj_name>/attendance/', AttendanceForAll.as_view(), name='all'),
    path('teacher/<str:teachername>/subject/<str:sbj_name>/attendance/<str:st_name>', AttendanceView.as_view(), name='att'),
    path('teacher/<str:teachername>/subject/<str:sbj_name>/attendance/<str:st_name>/<pk>/', AttendanceUpdateView.as_view(), name='ptscr'),

    path('subjects/', AllSubjectList.as_view(), name='subjects'),
    path('subjects/<str:sbj_name>/', StudentList.as_view(), name='namestu'),
    path('subjects/<str:sbj_name>/attendance/', AttendanceForAll.as_view(), name='namesubj'),
    path('subjects/<str:sbj_name>/<str:st_name>/rate/', AttendanceView.as_view(), name='rate'),
    path('subjects/<str:sbj_name>/<str:st_name>/rate/<pk>/', AttendanceUpdateView.as_view(), name='date')
]