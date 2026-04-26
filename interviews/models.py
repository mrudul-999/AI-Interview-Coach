from django.db import models
from django.contrib.auth.models import User

class InterviewSession(models.Model):
    # 1. The Relationship: Links this session to the logged-in User
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 2. The Structured Resume Data
    candidate_skills = models.TextField(blank=True)
    candidate_college = models.CharField(max_length=255, blank=True)
    candidate_past_exp = models.TextField(blank=True)
    candidate_tech_stack = models.TextField(blank=True)
    
    # 3. The Structured Job Description Data
    job_role_name = models.CharField(max_length=255)
    job_skills_needed = models.TextField(blank=True)
    
    # Metadata          
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.job_role_name}"

class InterviewQuestion(models.Model):
    # Link back to the Session
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name="questions")
    
    # 1. The Question
    question_text = models.TextField()
    category = models.CharField(max_length=50, blank=True) # e.g. 'technical', 'behavioral', 'experience'
    
    # 2. The User's Answer
    user_answer = models.TextField(blank=True) # Blank initially because they haven't answered yet
    
    # 3. The AI Evaluation
    ai_feedback = models.TextField(blank=True)
    score = models.IntegerField(null=True, blank=True) # e.g., 1 to 10
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question for {self.session.candidate.username} - {self.category}"
