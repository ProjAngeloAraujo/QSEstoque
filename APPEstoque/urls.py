from django.urls import path
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_user(request):
    logout(request)
    return redirect('index')


urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password/', views.password, name='password'),
    path('container/', views.container, name='container'),
    path('logout/', logout_user, name='logout_user')
]