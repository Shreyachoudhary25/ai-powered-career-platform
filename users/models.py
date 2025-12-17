from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    university = models.CharField(max_length=150)
    course = models.CharField(max_length=100)

    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

