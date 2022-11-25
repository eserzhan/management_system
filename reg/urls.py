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
    path('teacher/', TeacherList.as_view(), name='tea'),
    path('teacher/<str:teachername>/subject/', StudentList.as_view(), name='subject'),
    path('teacher/<str:teachername>/subject/<str:subj>/', StudentList.as_view(), name='stu'),
    path('teacher/<str:teachername>/subject/<str:subj>/attendance/<str:stud>', StudentList.as_view(), name='att'),
    path('attendance/', SubjectList.as_view(), name='attendmark'),
    path('attendance/<str:subjname>/', Student.as_view(), name='namesubj'),
    path('attendance/<str:subjname>/<str:stud>/', AttendanceCreate.as_view(), name='namestu'),
    path('students', manage_students, name="students"),
    path('students/<slug:key>', manage_student, name="single_student")
]