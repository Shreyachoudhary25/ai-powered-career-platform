from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobSerializer
from rest_framework import status

from users.models import StudentProfile
from .models import Job, Application
from .models import Internship, InternshipApplication

from rest_framework.parsers import JSONParser, FormParser
from rest_framework.decorators import parser_classes
from django.shortcuts import get_object_or_404

from users.models import EmployerProfile
from .serializers import ApplicationSerializer

from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.decorators import renderer_classes







@api_view(['GET'])
def job_list_api(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

from .serializers import InternshipSerializer
from .models import Internship


@api_view(['GET'])
def internship_list_api(request):
    internships = Internship.objects.all()
    serializer = InternshipSerializer(internships, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@parser_classes([JSONParser, FormParser])
def apply_to_job_api(request, job_id):
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return Response(
            {"error": "Only students can apply"},
            status=status.HTTP_403_FORBIDDEN
        )

    job = get_object_or_404(Job, id=job_id)

    application, created = Application.objects.get_or_create(
        student=student,
        job=job
    )

    if not created:
        return Response(
            {"message": "Already applied"},
            status=status.HTTP_200_OK
        )

    return Response(
        {"message": "Application submitted successfully"},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@parser_classes([JSONParser, FormParser])
def apply_to_internship_api(request, internship_id):
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return Response(
            {"error": "Only students can apply"},
            status=status.HTTP_403_FORBIDDEN
        )

    internship = get_object_or_404(Internship, id=internship_id)

    application, created = InternshipApplication.objects.get_or_create(
        student=student,
        internship=internship
    )

    if not created:
        return Response(
            {"message": "Already applied"},
            status=status.HTTP_200_OK
        )

    return Response(
        {"message": "Internship application submitted"},
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def employer_applications_api(request):
    try:
        employer = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return Response(
            {"error": "Only employers can access this"},
            status=status.HTTP_403_FORBIDDEN
        )

    applications = Application.objects.filter(
        job__employer=employer
    ).select_related('student', 'job')

    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
@parser_classes([JSONParser, FormParser])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def update_application_status_api(request, application_id):

    try:
        employer = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return Response(
            {"error": "Only employers can update application status"},
            status=status.HTTP_403_FORBIDDEN
        )

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=employer
    )

    new_status = request.data.get('status')

    valid_statuses = dict(Application.STATUS_CHOICES)

    if new_status not in valid_statuses:
        return Response(
            {"error": "Invalid status"},
            status=status.HTTP_400_BAD_REQUEST
        )

    application.status = new_status
    application.save()

    return Response(
        {
            "message": "Application status updated",
            "application_id": application.id,
            "new_status": application.status
        },
        status=status.HTTP_200_OK
    )


