from django.contrib import admin
from .models import Subject, Lesson, LessonResource, UserProgress

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color_code')
    search_fields = ('name', 'description')

class LessonResourceInline(admin.TabularInline):
    model = LessonResource
    extra = 1

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'grade_level', 'difficulty', 'created_at')
    list_filter = ('subject', 'grade_level', 'difficulty', 'created_at')
    search_fields = ('title', 'description', 'content')
    inlines = [LessonResourceInline]

@admin.register(LessonResource)
class LessonResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'resource_type', 'created_at')
    list_filter = ('resource_type', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('lesson',)

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed', 'progress_percentage', 'last_accessed')
    list_filter = ('completed', 'last_accessed')
    search_fields = ('student__user__username', 'lesson__title')
    raw_id_fields = ('student', 'lesson')
