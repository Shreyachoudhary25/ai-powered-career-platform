from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import StudentProfile, EmployerProfile, MentorProfile


@receiver(m2m_changed, sender=User.groups.through)
def create_profile_on_group_add(sender, instance, action, pk_set, **kwargs):
    if action != "post_add":
        return

    # Students group
    if Group.objects.filter(id__in=pk_set, name="Students").exists():
        StudentProfile.objects.get_or_create(
            user=instance,
            defaults={"full_name": instance.username}
        )

    # Employers group
    if Group.objects.filter(id__in=pk_set, name="Employers").exists():
        EmployerProfile.objects.get_or_create(
            user=instance,
            defaults={"company_name": instance.username}
        )

    # Mentors group
    if Group.objects.filter(id__in=pk_set, name="Mentors").exists():
        MentorProfile.objects.get_or_create(
            user=instance,
            defaults={"full_name": instance.username}
        )