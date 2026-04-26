from django.urls import path
from django.contrib.auth import views as auth_views
from .views import StartSessionView, SubmitAnswerView, RegisterView, LoginView, dashboard_view, start_interview_view, submit_answer_html

urlpatterns = [
    #frontend page requests
    path('', dashboard_view, name='dashboard'),
    path('start-interview/', start_interview_view, name='start-interview'),
    
    path('submit-answer/<int:question_id>/', submit_answer_html, name='submit-answer-html'),

    #frontend auth pages
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login-page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout-page'),


    # Auth endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),

    
    # Interview endpoints
    path('api/sessions/', StartSessionView.as_view(), name='start-session'),
    path('api/questions/<int:question_id>/answer/', SubmitAnswerView.as_view(), name='submit-answer'),
]
