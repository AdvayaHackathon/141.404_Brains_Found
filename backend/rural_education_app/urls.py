"""
URL configuration for rural_education_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Import views from apps
from users.views import GradeLevelViewSet, StudentProfileViewSet, RegisterView, login_view, logout_view, change_password, get_current_user
from content.views import SubjectViewSet, LessonViewSet, LessonResourceViewSet, UserProgressViewSet
from assessment.views import AssessmentViewSet, QuestionViewSet, UserAssessmentViewSet, UserAnswerViewSet
from ai_assistant.views import AIModelViewSet, ChatSessionViewSet, ChatMessageViewSet, FrequentlyAskedQuestionViewSet

# Create a router for API endpoints
router = DefaultRouter()

# Users routes
router.register(r'grade-levels', GradeLevelViewSet)
router.register(r'student-profiles', StudentProfileViewSet)

# Content routes
router.register(r'subjects', SubjectViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'lesson-resources', LessonResourceViewSet)
router.register(r'user-progress', UserProgressViewSet, basename='user-progress')

# Assessment routes
router.register(r'assessments', AssessmentViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'user-assessments', UserAssessmentViewSet, basename='user-assessments')
router.register(r'user-answers', UserAnswerViewSet, basename='user-answers')

# AI Assistant routes
router.register(r'ai-models', AIModelViewSet)
router.register(r'chat-sessions', ChatSessionViewSet, basename='chat-sessions')
router.register(r'chat-messages', ChatMessageViewSet, basename='chat-messages')
router.register(r'faqs', FrequentlyAskedQuestionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/change-password/', change_password, name='change-password'),
    path('api/auth/me/', get_current_user, name='current-user'),
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
