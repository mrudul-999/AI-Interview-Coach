from django.urls import path
from .views import StartSessionView, SubmitAnswerView, RegisterView, LoginView

urlpatterns = [
    # Auth endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    
    # Interview endpoints
    path('api/sessions/', StartSessionView.as_view(), name='start-session'),
    path('api/questions/<int:question_id>/answer/', SubmitAnswerView.as_view(), name='submit-answer'),
]
