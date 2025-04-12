from django.db import models
from users.models import GradeLevel, StudentProfile
from content.models import Subject, Lesson

class Assessment(models.Model):
    PRACTICE = 'practice'
    QUIZ = 'quiz'
    EXAM = 'exam'

    ASSESSMENT_TYPE_CHOICES = [
        (PRACTICE, 'Practice Test'),
        (QUIZ, 'Quiz'),
        (EXAM, 'Graded Exam'),
    ]

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
    assessment_type = models.CharField(max_length=10, choices=ASSESSMENT_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assessments')
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, related_name='assessments')
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, default=BEGINNER)
    time_limit_minutes = models.IntegerField(default=30)
    passing_score = models.IntegerField(default=70)  # Percentage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    related_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='assessments')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.get_assessment_type_display()})"

class Question(models.Model):
    MULTIPLE_CHOICE = 'multiple_choice'
    TRUE_FALSE = 'true_false'
    SHORT_ANSWER = 'short_answer'

    QUESTION_TYPE_CHOICES = [
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (TRUE_FALSE, 'True/False'),
        (SHORT_ANSWER, 'Short Answer'),
    ]

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPE_CHOICES)
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    explanation = models.TextField(blank=True)  # Explanation shown after answering

    def __str__(self):
        return f"{self.assessment.title} - Q{self.order}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.question} - A{self.order} ({'Correct' if self.is_correct else 'Incorrect'})"

class UserAssessment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='assessments')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='user_assessments')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)  # Final score
    time_spent_seconds = models.IntegerField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_passed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.assessment.title}"

class UserAnswer(models.Model):
    user_assessment = models.ForeignKey(UserAssessment, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, related_name='user_selections')
    text_answer = models.TextField(blank=True)  # For short answer questions
    is_correct = models.BooleanField(null=True, blank=True)  # Null for short answer questions that need manual grading
    points_earned = models.IntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_assessment.student} - {self.question}"
