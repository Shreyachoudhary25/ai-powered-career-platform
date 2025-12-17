from django.db import models
from users.models import EmployerProfile


class Job(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=100)

    is_remote = models.BooleanField(default=False)
    salary = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Internship(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=150)
    description = models.TextField()
    duration_months = models.PositiveIntegerField()

    stipend = models.CharField(max_length=50, blank=True)
    is_remote = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
from users.models import StudentProfile


class Application(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('selected', 'Selected'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied'
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'job')

    def __str__(self):
        return f"{self.student.full_name} → {self.job.title}"

