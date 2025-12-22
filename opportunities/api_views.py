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
