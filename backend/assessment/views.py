from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Avg, Count
from .models import Assessment, Question, Answer, UserAssessment, UserAnswer
from .serializers import (
    AssessmentSerializer, AssessmentListSerializer, QuestionSerializer,
    AnswerSerializer, UserAssessmentSerializer, UserAssessmentListSerializer,
    UserAnswerSerializer
)

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.filter(is_active=True)
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return AssessmentListSerializer
        return AssessmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def filter_assessments(self, request):
        grade_level = request.query_params.get('grade_level')
        subject = request.query_params.get('subject')
        assessment_type = request.query_params.get('assessment_type')
        difficulty = request.query_params.get('difficulty')

        queryset = self.get_queryset()

        if grade_level:
            queryset = queryset.filter(grade_level__name=grade_level)
        if subject:
            queryset = queryset.filter(subject__name=subject)
        if assessment_type:
            queryset = queryset.filter(assessment_type=assessment_type)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        serializer = AssessmentListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        assessment = self.get_object()
        questions = assessment.questions.all().order_by('order')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['get'])
    def answers(self, request, pk=None):
        question = self.get_object()
        answers = question.answers.all().order_by('order')
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

class UserAssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = UserAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAssessment.objects.filter(student=self.request.user.student_profile)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserAssessmentListSerializer
        return UserAssessmentSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        user_assessment = self.get_object()

        if user_assessment.is_completed:
            return Response({'error': 'Assessment already completed'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate score
        total_questions = user_assessment.assessment.questions.count()
        correct_answers = user_assessment.user_answers.filter(is_correct=True).count()

        if total_questions > 0:
            score = (correct_answers / total_questions) * 100
        else:
            score = 0

        # Update user assessment
        user_assessment.score = score
        user_assessment.is_completed = True
        user_assessment.completed_at = timezone.now()
        user_assessment.is_passed = score >= user_assessment.assessment.passing_score
        user_assessment.save()

        serializer = UserAssessmentSerializer(user_assessment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_assessments(self, request):
        student_profile = request.user.student_profile
        assessments = UserAssessment.objects.filter(student=student_profile)
        serializer = UserAssessmentListSerializer(assessments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        student_profile = request.user.student_profile
        completed_assessments = UserAssessment.objects.filter(
            student=student_profile,
            is_completed=True
        )

        stats = {
            'total_completed': completed_assessments.count(),
            'total_passed': completed_assessments.filter(is_passed=True).count(),
            'average_score': completed_assessments.aggregate(avg_score=Avg('score'))['avg_score'] or 0,
            'by_type': {}
        }

        # Get stats by assessment type
        assessment_types = ['practice', 'quiz', 'exam']
        for assessment_type in assessment_types:
            type_assessments = completed_assessments.filter(assessment__assessment_type=assessment_type)
            stats['by_type'][assessment_type] = {
                'completed': type_assessments.count(),
                'passed': type_assessments.filter(is_passed=True).count(),
                'average_score': type_assessments.aggregate(avg_score=Avg('score'))['avg_score'] or 0
            }

        return Response(stats)

class UserAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAnswer.objects.filter(user_assessment__student=self.request.user.student_profile)

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        selected_answer = serializer.validated_data.get('selected_answer')
        text_answer = serializer.validated_data.get('text_answer', '')

        # Determine if the answer is correct
        is_correct = False
        points_earned = 0

        if question.question_type in ['multiple_choice', 'true_false']:
            if selected_answer and selected_answer.is_correct:
                is_correct = True
                points_earned = question.points
        elif question.question_type == 'short_answer':
            # For short answer, we'll need manual grading or more sophisticated checking
            # For now, we'll leave it as not graded
            is_correct = None

        serializer.save(
            is_correct=is_correct,
            points_earned=points_earned
        )
