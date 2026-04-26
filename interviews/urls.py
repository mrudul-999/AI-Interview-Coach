from django.urls import path
from .views import StartSessionView, SubmitAnswerView, RegisterView, LoginView, dashboard_view, start_interview_view, submit_answer_html

urlpatterns = [
    #frontend page requests
    path('', dashboard_view, name='dashboard'),
    path('start-interview/', start_interview_view, name='start-interview'),
    
    path('submit-answer/<int:question_id>/', submit_answer_html, name='submit-answer-html'),


    # Auth endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),

    
    # Interview endpoints
    path('api/sessions/', StartSessionView.as_view(), name='start-session'),
    path('api/questions/<int:question_id>/answer/', SubmitAnswerView.as_view(), name='submit-answer'),
]
