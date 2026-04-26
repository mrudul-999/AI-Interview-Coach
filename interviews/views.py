from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InterviewSessionSerializer
from .services import generate_interview_questions
from .models import InterviewQuestion
from django.contrib.auth.decorators import login_required

class StartSessionView(APIView):
    def post(self, request):
        # 1. Check if the incoming JSON data is valid
        serializer = InterviewSessionSerializer(data=request.data)
        if serializer.is_valid():
            
            # 2. Save the Session to the database (linked to the logged in user)
            # NOTE: For now we'll hardcode the first user since we haven't done login yet
            from django.contrib.auth.models import User
            user = User.objects.first() 
            session = serializer.save(candidate=user)
            
            # 3. Call our AI Brain to get 3 questions
            ai_questions = generate_interview_questions(
                role_name=session.job_role_name,
                skills_needed=session.job_skills_needed
            )
            
            # 4. Save those 3 questions to the database linked to this session
            for q_text in ai_questions:
                InterviewQuestion.objects.create(
                    session=session,
                    question_text=q_text,
                    category="AI Generated"
                )
            
            # 5. Send the full Session (now with questions!) back to the frontend
            return Response(InterviewSessionSerializer(session).data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
from .services import evaluate_answer
from .serializers import InterviewQuestionSerializer

class SubmitAnswerView(APIView):
    def post(self, request, question_id):
        # 1. Get the exact question from the database
        question = get_object_or_404(InterviewQuestion, id=question_id)
        
        # 2. Grab the user's typed answer from the incoming JSON
        user_answer = request.data.get("answer")
        if not user_answer:
            return Response({"error": "Answer cannot be blank"}, status=status.HTTP_400_BAD_REQUEST)
            
        # 3. Save their answer to the database
        question.user_answer = user_answer
        question.save()
        
        # 4. Ask our AI Brain to grade it!
        score, feedback = evaluate_answer(question.question_text, user_answer)
        
        # 5. Fill in those blank columns and save again
        question.score = score
        question.ai_feedback = feedback
        question.save()
        
        # 6. Send the updated question (with grades!) back to the frontend
        return Response(InterviewQuestionSerializer(question).data)

from django.contrib.auth import authenticate, login, logout
from .serializers import UserRegistrationSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Check if the username and password match the database
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # This magically creates a secure session and sends a cookie to the browser!
            login(request, user)
            return Response({"message": f"Welcome back, {user.username}!"})
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


from django.shortcuts import render

@login_required
def dashboard_view(request):
    past_sessions = InterviewSession.objects.filter(candidate=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'past_sessions': past_sessions})


from .models import InterviewSession, InterviewQuestion
from .services import generate_interview_questions

@login_required
def start_interview_view(request):
    if request.method == "POST":
        role = request.POST.get('job_role_name')
        skills = request.POST.get('job_skills_needed')
        
        # 1. Create Session
        user = request.user 
        session = InterviewSession.objects.create(candidate=user, job_role_name=role, job_skills_needed=skills)
        
        # 2. Ask Gemini
        ai_questions = generate_interview_questions(role, skills)
        
        # 3. Save Questions
        for q_text in ai_questions:
            InterviewQuestion.objects.create(session=session, question_text=q_text, category="AI Generated")
            
        # 4. Return the new HTML Arena!
        return render(request, 'interview_arena.html', {'session': session})


from django.shortcuts import get_object_or_404
from .services import evaluate_answer

def submit_answer_html(request, question_id):
    if request.method == "POST":
        question = get_object_or_404(InterviewQuestion, id=question_id)
        user_answer = request.POST.get('answer')
        
        # 1. Ask Gemini to grade it
        score, feedback = evaluate_answer(question.question_text, user_answer)
        
        # 2. Save to database
        question.user_answer = user_answer
        question.score = score
        question.ai_feedback = feedback
        question.save()
        
        # 3. Return the feedback HTML!
        return render(request, 'partials/feedback.html', {'question': question})
