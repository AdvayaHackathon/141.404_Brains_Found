from django.contrib import admin
from .models import AIModel, ChatSession, ChatMessage, FrequentlyAskedQuestion

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'size_mb', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('message_type', 'content', 'timestamp')

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'subject', 'created_at', 'last_activity', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('student__user__username', 'title')
    raw_id_fields = ('student', 'subject')
    inlines = [ChatMessageInline]

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'message_type', 'content_preview', 'timestamp')
    list_filter = ('message_type', 'timestamp')
    search_fields = ('content', 'session__title')
    raw_id_fields = ('session',)
    readonly_fields = ('timestamp',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'subject', 'grade_level', 'created_at', 'updated_at')
    list_filter = ('subject', 'grade_level', 'created_at')
    search_fields = ('question', 'answer')

    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question Preview'
