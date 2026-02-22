from rest_framework.permissions import BasePermission
from users.models import StudentProfile, EmployerProfile, MentorProfile


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return StudentProfile.objects.filter(user=request.user).exists()


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return EmployerProfile.objects.filter(user=request.user).exists()
    
class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return MentorProfile.objects.filter(user=request.user).exists()
    
