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
    path('teacher/<str:teachername>/subject/<str:subj>/attendance/<str:stud>', StudentList.as_view(), name='att')
]