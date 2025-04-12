from django.contrib import admin
from .models import Assessment, Question, Answer, UserAssessment, UserAnswer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'question_text', 'question_type', 'points', 'order')
    list_filter = ('question_type', 'assessment')
    search_fields = ('question_text', 'explanation')
    inlines = [AnswerInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'assessment_type', 'subject', 'grade_level', 'difficulty', 'created_at')
    list_filter = ('assessment_type', 'subject', 'grade_level', 'difficulty', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('related_lesson',)
    inlines = [QuestionInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text', 'is_correct', 'order')
    list_filter = ('is_correct',)
    search_fields = ('answer_text',)
    raw_id_fields = ('question',)

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ('question', 'selected_answer', 'text_answer', 'is_correct', 'points_earned', 'answered_at')

@admin.register(UserAssessment)
class UserAssessmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'assessment', 'started_at', 'completed_at', 'score', 'is_completed', 'is_passed')
    list_filter = ('is_completed', 'is_passed', 'started_at')
    search_fields = ('student__user__username', 'assessment__title')
    raw_id_fields = ('student', 'assessment')
    readonly_fields = ('started_at', 'completed_at', 'score', 'time_spent_seconds', 'is_completed', 'is_passed')
    inlines = [UserAnswerInline]

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user_assessment', 'question', 'selected_answer', 'is_correct', 'points_earned', 'answered_at')
    list_filter = ('is_correct', 'answered_at')
    search_fields = ('user_assessment__student__user__username', 'question__question_text')
    raw_id_fields = ('user_assessment', 'question', 'selected_answer')
    readonly_fields = ('is_correct', 'points_earned', 'answered_at')
