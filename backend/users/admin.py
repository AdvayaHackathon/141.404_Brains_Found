from django.contrib import admin
from .models import GradeLevel, StudentProfile

@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'grade_level', 'date_of_birth', 'parent_mobile', 'date_joined', 'last_login')
    list_filter = ('grade_level', 'date_joined')
    search_fields = ('user__username', 'user__email', 'student_id', 'parent_mobile')
    raw_id_fields = ('user',)
