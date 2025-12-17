from django.contrib import admin
from .models import Job, Internship, Application, InternshipApplication

admin.site.register(Job)
admin.site.register(Internship)
admin.site.register(Application)
admin.site.register(InternshipApplication)


