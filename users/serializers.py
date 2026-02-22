from rest_framework import serializers
from .models import MentorProfile, MentorshipRequest


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorProfile
        fields = ['id', 'full_name', 'expertise', 'experience_years', 'bio', 'linkedin']


class MentorshipRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    mentor_name = serializers.CharField(source='mentor.full_name', read_only=True)

    class Meta:
        model = MentorshipRequest
        fields = ['id', 'student_name', 'mentor_name', 'status', 'created_at']