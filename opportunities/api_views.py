from rest_framework.decorators import api_view, parser_classes, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from django.shortcuts import get_object_or_404

from .models import Job, Application, Internship, InternshipApplication
from .serializers import JobSerializer, InternshipSerializer, ApplicationSerializer
from .permissions import IsStudent, IsEmployer

from users.models import StudentProfile, EmployerProfile

from users.models import MentorProfile, MentorshipRequest
from users.serializers import MentorSerializer, MentorshipRequestSerializer
from .permissions import IsMentor


# ---------------- JOB LIST ----------------

@api_view(['GET'])
def job_list_api(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)
# ---------------- INTERNSHIP LIST ----------------

@api_view(['GET'])
def internship_list_api(request):
    internships = Internship.objects.all()
    serializer = InternshipSerializer(internships, many=True)
    return Response(serializer.data)


# ---------------- APPLY TO JOB ----------------

@api_view(['POST'])
@permission_classes([IsStudent])
@parser_classes([JSONParser, FormParser])
def apply_to_job_api(request, job_id):

    student = StudentProfile.objects.get(user=request.user)
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


# ---------------- APPLY TO INTERNSHIP ----------------

@api_view(['POST'])
@permission_classes([IsStudent])
@parser_classes([JSONParser, FormParser])
def apply_to_internship_api(request, internship_id):

    student = StudentProfile.objects.get(user=request.user)
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


# ---------------- EMPLOYER VIEW APPLICATIONS ----------------

@api_view(['GET'])
@permission_classes([IsEmployer])
def employer_applications_api(request):

    employer = EmployerProfile.objects.get(user=request.user)

    applications = Application.objects.filter(
        job__employer=employer
    ).select_related('student', 'job')

    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)


# ---------------- UPDATE APPLICATION STATUS ----------------

@api_view(['POST'])
@permission_classes([IsEmployer])
@parser_classes([JSONParser, FormParser])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def update_application_status_api(request, application_id):

    employer = EmployerProfile.objects.get(user=request.user)

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

@api_view(['GET'])
def mentor_list_api(request):
    mentors = MentorProfile.objects.all()
    serializer = MentorSerializer(mentors, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsStudent])
def send_mentorship_request_api(request, mentor_id):

    student = StudentProfile.objects.get(user=request.user)
    mentor = get_object_or_404(MentorProfile, id=mentor_id)

    request_obj, created = MentorshipRequest.objects.get_or_create(
        student=student,
        mentor=mentor
    )

    if not created:
        return Response(
            {"message": "Request already sent"},
            status=status.HTTP_200_OK
        )

    return Response(
        {"message": "Mentorship request sent"},
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([IsMentor])
def mentor_requests_api(request):

    mentor = MentorProfile.objects.get(user=request.user)

    requests = MentorshipRequest.objects.filter(
        mentor=mentor
    ).select_related('student')

    serializer = MentorshipRequestSerializer(requests, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsMentor])
def update_mentorship_status_api(request, request_id):

    mentor = MentorProfile.objects.get(user=request.user)

    mentorship_request = get_object_or_404(
        MentorshipRequest,
        id=request_id,
        mentor=mentor
    )

    new_status = request.data.get('status')

    valid_statuses = dict(MentorshipRequest.STATUS_CHOICES)

    if new_status not in valid_statuses:
        return Response(
            {"error": "Invalid status"},
            status=status.HTTP_400_BAD_REQUEST
        )

    mentorship_request.status = new_status
    mentorship_request.save()

    return Response(
        {
            "message": "Mentorship request updated",
            "new_status": mentorship_request.status
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsStudent])
def student_mentorship_requests_api(request):

    student = StudentProfile.objects.get(user=request.user)

    requests = MentorshipRequest.objects.filter(
        student=student
    ).select_related('mentor')

    data = [
        {
            "id": r.id,
            "mentor": r.mentor.full_name,
            "status": r.status,
            "created_at": r.created_at
        }
        for r in requests
    ]

    return Response(data)

@api_view(['GET'])
@permission_classes([IsMentor])
def mentor_received_requests_api(request):

    mentor = MentorProfile.objects.get(user=request.user)

    requests = MentorshipRequest.objects.filter(
        mentor=mentor
    ).select_related('student')

    data = [
        {
            "id": r.id,
            "student": r.student.full_name,
            "status": r.status,
            "created_at": r.created_at
        }
        for r in requests
    ]

    return Response(data)




