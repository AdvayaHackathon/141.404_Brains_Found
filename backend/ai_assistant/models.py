from django.db import models
from users.models import StudentProfile
from content.models import Subject

class AIModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    model_file = models.FileField(upload_to='ai_models/')
    version = models.CharField(max_length=20)
    size_mb = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} v{self.version}"

class ChatSession(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='chat_sessions')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_sessions')
    title = models.CharField(max_length=200, default='New Chat')
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student} - {self.title}"

class ChatMessage(models.Model):
    USER = 'user'
    AI = 'ai'

    MESSAGE_TYPE_CHOICES = [
        (USER, 'User'),
        (AI, 'AI Assistant'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=4, choices=MESSAGE_TYPE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.session} - {self.get_message_type_display()} ({self.timestamp})"

class FrequentlyAskedQuestion(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='faqs')
    grade_level = models.CharField(max_length=20)  # Store as '1', '2', '3', '4', '5' for elementary grades
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
