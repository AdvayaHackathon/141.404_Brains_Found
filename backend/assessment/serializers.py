from rest_framework import serializers
from .models import Assessment, Question, Answer, UserAssessment, UserAnswer
from users.serializers import StudentProfileSerializer, GradeLevelSerializer
from users.models import GradeLevel
from content.serializers import SubjectSerializer, LessonSerializer
from content.models import Subject

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct', 'order']
        read_only_fields = ['id']
        extra_kwargs = {
            'is_correct': {'write_only': True}  # Hide correct answers from students
        }

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'points', 'order', 'explanation', 'answers']
        read_only_fields = ['id']

class AssessmentSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject',
        write_only=True
    )
    grade_level = GradeLevelSerializer(read_only=True)
    grade_level_id = serializers.PrimaryKeyRelatedField(
        queryset=GradeLevel.objects.all(),
        source='grade_level',
        write_only=True
    )
    questions = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = [
            'id', 'title', 'description', 'assessment_type', 'subject', 'subject_id',
            'grade_level', 'grade_level_id', 'difficulty', 'time_limit_minutes',
            'passing_score', 'created_at', 'updated_at',
            'related_lesson', 'is_active', 'questions', 'question_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_question_count(self, obj):
        return obj.questions.count()

class AssessmentListSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    grade_level = GradeLevelSerializer(read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = [
            'id', 'title', 'description', 'assessment_type', 'subject',
            'grade_level', 'difficulty', 'time_limit_minutes', 'question_count'
        ]

    def get_question_count(self, obj):
        return obj.questions.count()

class UserAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(),
        source='question',
        write_only=True
    )
    selected_answer = AnswerSerializer(read_only=True)
    selected_answer_id = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(),
        source='selected_answer',
        write_only=True,
        required=False
    )

    class Meta:
        model = UserAnswer
        fields = [
            'id', 'question', 'question_id', 'selected_answer', 'selected_answer_id',
            'text_answer', 'is_correct', 'points_earned', 'answered_at'
        ]
        read_only_fields = ['id', 'is_correct', 'points_earned', 'answered_at']

class UserAssessmentSerializer(serializers.ModelSerializer):
    assessment = AssessmentSerializer(read_only=True)
    assessment_id = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all(),
        source='assessment',
        write_only=True
    )
    student = StudentProfileSerializer(read_only=True)
    user_answers = UserAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = UserAssessment
        fields = [
            'id', 'student', 'assessment', 'assessment_id', 'started_at',
            'completed_at', 'score', 'time_spent_seconds', 'is_completed',
            'is_passed', 'user_answers'
        ]
        read_only_fields = ['id', 'student', 'started_at', 'score', 'is_passed']

class UserAssessmentListSerializer(serializers.ModelSerializer):
    assessment = AssessmentListSerializer(read_only=True)

    class Meta:
        model = UserAssessment
        fields = [
            'id', 'assessment', 'started_at', 'completed_at',
            'score', 'is_completed', 'is_passed'
        ]
