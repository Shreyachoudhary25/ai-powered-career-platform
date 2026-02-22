from django.urls import path

# Template Views
from .views import (
    home,
    employer_applications,
    update_application_status,
    job_list,
    apply_to_job,
    student_applications,
    employer_dashboard,
    internship_list,
    apply_to_internship,
)

# API Views
from .api_views import (
    job_list_api,
    internship_list_api,
    apply_to_job_api,
    apply_to_internship_api,
    employer_applications_api,
    update_application_status_api,

    mentor_list_api,
    send_mentorship_request_api,
    student_mentorship_requests_api,
    mentor_received_requests_api,
    update_mentorship_status_api,
)

urlpatterns = [

    # =========================
    # Template Routes (Frontend)
    # =========================

    path('', home, name='home'),

    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/apply/', apply_to_job, name='apply_to_job'),

    path('internships/', internship_list, name='internship_list'),
    path('internships/<int:internship_id>/apply/', apply_to_internship, name='apply_to_internship'),

    path('student/applications/', student_applications, name='student_applications'),

    path('employer/dashboard/', employer_dashboard, name='employer_dashboard'),
    path('employer/applications/', employer_applications, name='employer_applications'),
    path('employer/applications/<int:app_id>/update/', update_application_status, name='update_application_status'),


    # =========================
    # API Routes
    # =========================

    # Jobs & Internships
    path('api/jobs/', job_list_api),
    path('api/internships/', internship_list_api),

    path('api/jobs/<int:job_id>/apply/', apply_to_job_api),
    path('api/internships/<int:internship_id>/apply/', apply_to_internship_api),

    # Employer APIs
    path('api/employer/applications/', employer_applications_api),
    path('api/employer/applications/<int:application_id>/update/', update_application_status_api),

    # =========================
    # Mentorship APIs
    # =========================

    # List all mentors
    path('api/mentors/', mentor_list_api),

    # Student sends request
    path('api/mentors/<int:mentor_id>/request/', send_mentorship_request_api),

    # Student views own requests
    path('api/student/mentorship-requests/', student_mentorship_requests_api),

    # Mentor views received requests
    path('api/mentor/requests/', mentor_received_requests_api),

    # Mentor updates request status
    path('api/mentor/requests/<int:request_id>/update/', update_mentorship_status_api),
]