from rest_framework import serializers
from .models import InterviewSession, InterviewQuestion

class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = ['id', 'question_text', 'category', 'user_answer', 'ai_feedback', 'score']

class InterviewSessionSerializer(serializers.ModelSerializer):
    questions = InterviewQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = InterviewSession
        fields = ['id', 'candidate', 'candidate_skills', 'job_role_name', 'job_skills_needed', 'questions', 'created_at']
        read_only_fields = ['candidate']

from django.contrib.auth.models import User
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # We MUST use create_user() so Django knows to cryptographically hash the password!
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
