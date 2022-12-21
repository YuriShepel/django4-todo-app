from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


def home(request):
    return render(request, 'todo/home.html')


def signup_user(request):
    if request.method == 'GET':
        context = {'form': UserCreationForm()}
        return render(request, 'todo/signup_user.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                context = {'form': UserCreationForm(),
                           'error': 'This name already exists'}
                return render(request, 'todo/signup_user.html', context)
        else:
            context = {'form': UserCreationForm(),
                       'error': 'Passwords did not mach'}
            return render(request, 'todo/signup_user.html', context)


def login_user(request):
    if request.method == 'GET':
        context = {'form': AuthenticationForm()}
        return render(request, 'todo/login_user.html', context)
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = {'form': AuthenticationForm(),
                       'error': 'Username and passwords did not mach'}
            return render(request, 'todo/login_user.html', context)
        else:
            login(request, user)
            return redirect('current_todos')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def current_todos(request):
    return render(request, 'todo/current_todos.html')
