from django.urls import path
from .views import (
    employer_applications,
    update_application_status,
    job_list,
    apply_to_job,
    student_applications,
)

urlpatterns = [
    path('employer/applications/', employer_applications, name='employer_applications'),
    path('employer/applications/<int:app_id>/update/', update_application_status, name='update_application_status'),

    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/apply/', apply_to_job, name='apply_to_job'),
    path('student/applications/', student_applications, name='student_applications'),

]
