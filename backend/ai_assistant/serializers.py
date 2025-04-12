from rest_framework import serializers
from .models import AIModel, ChatSession, ChatMessage, FrequentlyAskedQuestion
from users.serializers import StudentProfileSerializer
from content.serializers import SubjectSerializer
from content.models import Subject

class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = ['id', 'name', 'description', 'version', 'size_mb', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'message_type', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class ChatSessionSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject',
        write_only=True,
        required=False
    )
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'student', 'subject', 'subject_id', 'title', 'created_at', 'last_activity', 'is_active', 'messages']
        read_only_fields = ['id', 'student', 'created_at', 'last_activity']

class ChatSessionListSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'subject', 'created_at', 'last_activity', 'is_active', 'message_count']

    def get_message_count(self, obj):
        return obj.messages.count()

class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject',
        write_only=True
    )

    class Meta:
        model = FrequentlyAskedQuestion
        fields = ['id', 'subject', 'subject_id', 'grade_level', 'question', 'answer', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
