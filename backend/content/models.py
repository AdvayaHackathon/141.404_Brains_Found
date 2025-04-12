from django.db import models
from users.models import GradeLevel, StudentProfile

class Subject(models.Model):
    MATH = 'mathematics'
    SCIENCE = 'science'
    LANGUAGE = 'language'
    HISTORY = 'history'
    COMPUTER_SCIENCE = 'computer_science'

    SUBJECT_CHOICES = [
        (MATH, 'Mathematics'),
        (SCIENCE, 'Science'),
        (LANGUAGE, 'Language'),
        (HISTORY, 'History'),
        (COMPUTER_SCIENCE, 'Computer Science'),
    ]

    name = models.CharField(max_length=20, choices=SUBJECT_CHOICES, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # CSS class for icon
    color_code = models.CharField(max_length=7, default='#3498db')  # Hex color code

    def __str__(self):
        return self.get_name_display()

class Lesson(models.Model):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'

    DIFFICULTY_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, related_name='lessons')
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, default=BEGINNER)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_downloadable = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class LessonResource(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'
    DOCUMENT = 'document'
    AUDIO = 'audio'

    RESOURCE_TYPE_CHOICES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (DOCUMENT, 'Document'),
        (AUDIO, 'Audio'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    file = models.FileField(upload_to='lesson_resources/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"

class UserProgress(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    progress_percentage = models.IntegerField(default=0)  # 0-100
    last_accessed = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} - {self.lesson.title} ({self.progress_percentage}%)"
