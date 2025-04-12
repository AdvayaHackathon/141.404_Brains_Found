from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import AIModel, ChatSession, ChatMessage, FrequentlyAskedQuestion
from .serializers import (
    AIModelSerializer, ChatSessionSerializer, ChatSessionListSerializer,
    ChatMessageSerializer, FrequentlyAskedQuestionSerializer
)

# Import the offline AI assistant
from django.conf import settings
import random
from .offline_ai import offline_ai

class AIModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AIModel.objects.filter(is_active=True)
    serializer_class = AIModelSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(student=self.request.user.student_profile, is_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatSessionListSerializer
        return ChatSessionSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        session = self.get_object()
        message_content = request.data.get('message', '')

        if not message_content:
            return Response({'error': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            message_type=ChatMessage.USER,
            content=message_content
        )

        # Generate AI response (this would be replaced with actual AI model)
        ai_response = self.generate_ai_response(message_content, session.subject)

        # Save AI response
        ai_message = ChatMessage.objects.create(
            session=session,
            message_type=ChatMessage.AI,
            content=ai_response
        )

        # Update session last activity
        session.last_activity = timezone.now()
        session.save()

        return Response({
            'user_message': ChatMessageSerializer(user_message).data,
            'ai_message': ChatMessageSerializer(ai_message).data
        })

    def generate_ai_response(self, message, subject):
        # Try to use the offline AI assistant first
        if offline_ai.is_available:
            try:
                # Get user ID from the request
                user_id = self.request.user.id

                # Get response from offline AI
                ai_response = offline_ai.get_response(user_id, message)

                # If successful, return the content
                if not ai_response.get('error'):
                    return ai_response.get('content')
            except Exception as e:
                print(f"Error using offline AI: {e}")
                # Fall back to simple responses if there's an error
                pass

        # Fallback responses for demonstration or when offline AI is not available
        elementary_responses = {
            'mathematics': [
                "Let me help you with that math problem. In elementary math, we focus on addition, subtraction, multiplication, and division.",
                "That's a good math question! Remember that numbers are our friends.",
                "In math, we learn to count, add, subtract, and solve simple problems."
            ],
            'science': [
                "Science is all about exploring the world around us. Plants, animals, and weather are all part of science!",
                "In elementary science, we learn about living things, the earth, and simple experiments.",
                "That's an interesting science question! Let's explore how things work in our world."
            ],
            'language': [
                "Reading and writing are important skills. Let's work on your language question.",
                "In language arts, we learn about letters, words, sentences, and stories.",
                "That's a great question about language! Let's explore words and their meanings."
            ],
            'history': [
                "History helps us learn about people and events from the past.",
                "In elementary history, we learn about our community, country, and important historical figures.",
                "That's an interesting history question! Let's explore what happened in the past."
            ]
        }

        generic_responses = [
            "I'm here to help with your educational questions.",
            "That's an interesting question. Let me explain...",
            "I understand your question. Here's what I know about that topic...",
            "Great question! The answer involves several concepts...",
            "I can help you understand this better. Let's break it down..."
        ]

        # If we have a subject, try to give a subject-specific response
        if subject and subject.name in elementary_responses:
            return random.choice(elementary_responses[subject.name])

        # Otherwise, give a generic response
        return random.choice(generic_responses)

    @action(detail=False, methods=['get'])
    def my_sessions(self, request):
        student_profile = request.user.student_profile
        sessions = ChatSession.objects.filter(student=student_profile, is_active=True)
        serializer = ChatSessionListSerializer(sessions, many=True)
        return Response(serializer.data)

class ChatMessageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(session__student=self.request.user.student_profile)

class FrequentlyAskedQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FrequentlyAskedQuestion.objects.all()
    serializer_class = FrequentlyAskedQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['question', 'answer']

    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        subject_id = request.query_params.get('subject_id')
        if subject_id:
            faqs = self.get_queryset().filter(subject_id=subject_id)
            serializer = self.get_serializer(faqs, many=True)
            return Response(serializer.data)
        return Response({'error': 'Subject ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_grade(self, request):
        grade = request.query_params.get('grade')
        if grade:
            faqs = self.get_queryset().filter(grade_level=grade)
            serializer = self.get_serializer(faqs, many=True)
            return Response(serializer.data)
        return Response({'error': 'Grade level is required'}, status=status.HTTP_400_BAD_REQUEST)
