from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.contrib.auth.models import User, Group

from .models import MentorProfile, MentorshipRequest
from users.models import StudentProfile


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


@login_required
def mentor_list(request):
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return HttpResponseForbidden("You are not a student.")

    mentors = MentorProfile.objects.all()

    requested_mentors = MentorshipRequest.objects.filter(
        student=student
    ).values_list('mentor_id', flat=True)

    return render(
        request,
        'users/mentor_list.html',
        {
            'mentors': mentors,
            'requested_mentors': requested_mentors
        }
    )

@login_required
@require_POST
def send_mentorship_request(request, mentor_id):
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return HttpResponseForbidden("You are not a student.")

    mentor = get_object_or_404(MentorProfile, id=mentor_id)

    MentorshipRequest.objects.get_or_create(
        student=student,
        mentor=mentor
    )

    return redirect('mentor_list')
@login_required
def mentor_requests(request):
    try:
        mentor = MentorProfile.objects.get(user=request.user)
    except MentorProfile.DoesNotExist:
        return HttpResponseForbidden("You are not a mentor.")

    requests = MentorshipRequest.objects.filter(
        mentor=mentor
    ).select_related('student')

    return render(
        request,
        'users/mentor_requests.html',
        {'requests': requests}
    )
@login_required
@require_POST
def update_mentorship_status(request, request_id):
    try:
        mentor = MentorProfile.objects.get(user=request.user)
    except MentorProfile.DoesNotExist:
        return HttpResponseForbidden("You are not a mentor.")

    mentorship_request = get_object_or_404(
        MentorshipRequest,
        id=request_id,
        mentor=mentor
    )

    new_status = request.POST.get('status')
    if new_status in ['accepted', 'rejected']:
        mentorship_request.status = new_status
        mentorship_request.save()

    return redirect('mentor_requests')

