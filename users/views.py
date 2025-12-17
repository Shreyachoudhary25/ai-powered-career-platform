from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.http import require_POST
from django.template.loader import get_template

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(
                request,
                'users/login.html',
                {'error': 'Invalid credentials'}
            )

    return render(request, 'users/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # student / employer

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'users/signup.html',
                {'error': 'Username already exists'}
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        if role == 'student':
            group = Group.objects.get(name='Students')
        else:
            group = Group.objects.get(name='Employers')

        user.groups.add(group)

        login(request, user)
        return redirect('/')

    return render(request, 'users/signup.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

def test_template(request):
    get_template('users/signup.html')
    return HttpResponse("Template found")


