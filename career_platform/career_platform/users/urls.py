from django.urls import path
from .views import (
    signup,
    login_view,
    dashboard,
    chatbot_view,
    logout_view,
    CareerAssessmentView,
    RecommendationsView,
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard where users can view their information and chat
    path('chatbot/', chatbot_view, name='chatbot'),  # Endpoint for the chatbot
    path('logout/', logout_view, name='logout'),
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),  # View for career recommendations
    path('career-assessment/', CareerAssessmentView.as_view(), name='career_assessment'),  # Assessment for career paths
]
