from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from users.models import EmployerProfile
from .models import Application


@login_required
def employer_applications(request):
    try:
        employer = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return HttpResponseForbidden("You are not an employer.")

    applications = Application.objects.filter(
        job__employer=employer
    ).select_related('student', 'job')

    return render(
        request,
        'opportunities/employer_applications.html',
        {'applications': applications}
    )


@login_required
@require_POST
def update_application_status(request, app_id):
    try:
        employer = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return HttpResponseForbidden("You are not an employer.")

    application = get_object_or_404(
        Application,
        id=app_id,
        job__employer=employer
    )

    new_status = request.POST.get("status")
    if new_status in dict(Application.STATUS_CHOICES):
        application.status = new_status
        application.save()

    return redirect("employer_applications")
