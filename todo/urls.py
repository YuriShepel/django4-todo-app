from django.urls import path
from . import views

name_app = 'todo'

urlpatterns = [
    # Authorization
    path('signup/', views.signup_user, name='signup_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    # Todos
    path('current/', views.current_todos, name='current_todos'),
    path('', views.home, name='home'),
]
