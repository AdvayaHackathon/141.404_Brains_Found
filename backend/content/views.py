from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Subject, Lesson, LessonResource, UserProgress
from .serializers import (
    SubjectSerializer, LessonSerializer, LessonListSerializer,
    LessonResourceSerializer, UserProgressSerializer
)

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return LessonListSerializer
        return LessonSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def filter_lessons(self, request):
        grade_level = request.query_params.get('grade_level')
        subject = request.query_params.get('subject')
        difficulty = request.query_params.get('difficulty')

        queryset = self.get_queryset()

        if grade_level:
            queryset = queryset.filter(grade_level__name=grade_level)
        if subject:
            queryset = queryset.filter(subject__name=subject)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        serializer = LessonListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def resources(self, request, pk=None):
        lesson = self.get_object()
        resources = lesson.resources.all()
        serializer = LessonResourceSerializer(resources, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        lesson = self.get_object()
        if lesson.is_downloadable:
            # In a real implementation, we would prepare a downloadable package
            # For now, just return the lesson content
            return Response({
                'title': lesson.title,
                'content': lesson.content,
                'resources': LessonResourceSerializer(lesson.resources.all(), many=True).data
            })
        return Response({'error': 'No downloadable content available'}, status=status.HTTP_404_NOT_FOUND)

class LessonResourceViewSet(viewsets.ModelViewSet):
    queryset = LessonResource.objects.all()
    serializer_class = LessonResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class UserProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student_profile = self.request.user.student_profile
        return UserProgress.objects.filter(student=student_profile)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile)

    @action(detail=False, methods=['get'])
    def my_progress(self, request):
        student_profile = request.user.student_profile
        progress = UserProgress.objects.filter(student=student_profile)
        serializer = UserProgressSerializer(progress, many=True)
        return Response(serializer.data)
