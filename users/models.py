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
    
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=150)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
    
class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=150)
    experience_years = models.PositiveIntegerField()

    bio = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
class MentorshipRequest(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'mentor')

    def __str__(self):
        return f"{self.student.full_name} → {self.mentor.full_name}"

