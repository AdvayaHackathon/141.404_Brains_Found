from rest_framework import serializers
from .models import Subject, Lesson, LessonResource, UserProgress
from users.serializers import StudentProfileSerializer, GradeLevelSerializer

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'icon', 'color_code']

class LessonResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonResource
        fields = ['id', 'title', 'resource_type', 'file', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class LessonSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject',
        write_only=True
    )
    grade_level = GradeLevelSerializer(read_only=True)
    grade_level_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='grade_level',
        write_only=True
    )
    resources = LessonResourceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'subject', 'subject_id', 
            'grade_level', 'grade_level_id', 'difficulty', 'content',
            'created_at', 'updated_at', 'is_downloadable', 'resources'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class LessonListSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    grade_level = GradeLevelSerializer(read_only=True)
    resource_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'subject', 'grade_level', 
            'difficulty', 'created_at', 'is_downloadable', 'resource_count'
        ]
    
    def get_resource_count(self, obj):
        return obj.resources.count()

class UserProgressSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    lesson = LessonListSerializer(read_only=True)
    lesson_id = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(),
        source='lesson',
        write_only=True
    )
    
    class Meta:
        model = UserProgress
        fields = [
            'id', 'student', 'lesson', 'lesson_id', 'completed', 
            'progress_percentage', 'last_accessed', 'notes'
        ]
        read_only_fields = ['id', 'student', 'last_accessed']
