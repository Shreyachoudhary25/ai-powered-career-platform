from django.urls import path
from .views import home
from .api_views import job_list_api
from .api_views import internship_list_api
from .api_views import apply_to_job_api, apply_to_internship_api
from .api_views import employer_applications_api
from .api_views import update_application_status_api






from .views import (
    employer_applications,
    update_application_status,
    job_list,
    apply_to_job,
    student_applications,
    employer_dashboard,
    internship_list,
    apply_to_internship,

)

urlpatterns = [
    path('', home, name='home'),

    path('employer/applications/', employer_applications, name='employer_applications'),
    path('employer/applications/<int:app_id>/update/', update_application_status, name='update_application_status'),

    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/apply/', apply_to_job, name='apply_to_job'),
    path('student/applications/', student_applications, name='student_applications'),
    path('employer/dashboard/', employer_dashboard, name='employer_dashboard'),
    path('internships/', internship_list, name='internship_list'),
    path('internships/<int:internship_id>/apply/', apply_to_internship, name='apply_to_internship'),
    path('api/jobs/', job_list_api, name='job_list_api'),
    path('api/internships/', internship_list_api, name='internship_list_api'),
    path('api/jobs/<int:job_id>/apply/', apply_to_job_api, name='apply_to_job_api'),
    path('api/internships/<int:internship_id>/apply/', apply_to_internship_api, name='apply_to_internship_api'),
    path('api/employer/applications/', employer_applications_api, name='employer_applications_api'),
    path('api/employer/applications/<int:application_id>/update/',update_application_status_api,name='update_application_status_api'),

    
]
