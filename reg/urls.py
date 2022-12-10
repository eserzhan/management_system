from django.urls import path
from .views import *

urlpatterns = [
    path('', bas, name='home'),
    path('register/', RegisterUser.as_view(), name='BaseU'),
    path('register/<int:num>/', RegisterSelfSubject.as_view(), name='selfsubj'),
    path('register/<str:sl_url>/', RegisterActivity.as_view(), name='act'),
    
    path('<str:st_name>/mysubjects/', SubjectList.as_view(), name='mysubj'),
    path('<str:st_name>/mysubjects/<str:sbj_name>/attendance', AttendanceView.as_view(), name='mysubjdet'),

    path('login/', LoginUser.as_view(), name='log'),
    path('logout/', logout_user, name='logo'),

    path('users/', ArticleListView.as_view(), name='usr'),
    path('users/<pk>/update', UserUpdateView.as_view(), name='pkk'),

    path('teacher/', TeacherList.as_view(), name='tea'),
    path('teacher/<str:teachername>/subject/', SubjectList.as_view(), name='subject'),
    path('teacher/<str:teachername>/subject/<str:sbj_name>/', StudentList.as_view(), name='stu'),
    path('teacher/<str:teachername>/subject/<str:sbj_name>/attendance/', AttendanceForAll.as_view(), name='all'),
    path('teacher/<str:teachername>/subject/<str:sbj_name>/attendance/<str:st_name>', AttendanceView.as_view(), name='att'),
    #path('teacher/<str:teachername>/subject/<str:sbj_name>/attendance/<str:st_name>/create/', AttendanceCreate.as_view(), name='attcr'),
    path('teacher/<str:teachername>/subject/<str:sbj_name>/attendance/<str:st_name>/<pk>/', AttendanceUpdateView.as_view(), name='ptscr'),
#subj
    path('mysubjects/', SubjectList.as_view(), name='namesubj'),
    path('mysubjects/<str:sbj_name>/', StudentList.as_view(), name='namestu'),
    path('mysubjects/<str:sbj_name>/attendance/', AttendanceForAll.as_view(), name='namesubj'),
    #path('mysubjects/<str:sbj_name>/<str:st_name>/', AttendanceCreate.as_view(), name='namestu'),
    path('mysubjects/<str:sbj_name>/<str:st_name>/rate/', AttendanceView.as_view(), name='rate'),
    path('mysubjects/<str:sbj_name>/<str:st_name>/rate/<pk>/', AttendanceUpdateView.as_view(), name='date')
]