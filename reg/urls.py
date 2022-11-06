from django.urls import path
from .views import *
urlpatterns = [
    path('', bas, name = 'home'),
    path('register/', RegisterUser.as_view(), name='BaseU'),
    path('register/<str:sl_url>/', RegisterActivity.as_view(),name='act'),
    path('login/', LoginUser.as_view(),name='log'),
    path('logout/', logout_user,name='logo'),
    path('users/', ArticleListView.as_view(),name='usr'),
    path('users/<pk>/update', UserUpdateView.as_view(), name = 'pkk')
]