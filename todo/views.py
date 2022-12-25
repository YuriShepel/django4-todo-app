from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo


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


def create_todo(request):
    if request.method == 'GET':
        context = {'form': TodoForm()}
        return render(request, 'todo/create_todo.html', context)
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            context = {'form': TodoForm(),
                       'error': 'Bad data passed in', }
            return render(request, 'todo/create_todo.html', context)


def current_todos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    context = {'todos': todos}
    return render(request, 'todo/current_todos.html', context)


def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        context = {'todo': todo,
                   'form': form,
                   }
        return render(request, 'todo/view_todo.html', context)
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            context = {'todo': todo,
                       'form': form,
                       'error': 'Bad info'
                       }
            return render(request, 'todo/view_todo.html', context)