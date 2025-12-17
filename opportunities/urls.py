from django.urls import path
from .views import employer_applications, update_application_status

urlpatterns = [
    path('employer/applications/', employer_applications, name='employer_applications'),
    path(
        'employer/applications/<int:app_id>/update/',
        update_application_status,
        name='update_application_status'
    ),
]
