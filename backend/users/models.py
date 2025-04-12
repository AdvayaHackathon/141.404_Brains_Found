from django.db import models
from django.contrib.auth.models import User

class GradeLevel(models.Model):
    ELEMENTARY = 'elementary'
    MIDDLE_SCHOOL = 'middle_school'
    HIGH_SCHOOL = 'high_school'

    GRADE_CHOICES = [
        (ELEMENTARY, 'Elementary (Grades 1-5)'),
        (MIDDLE_SCHOOL, 'Middle School (Grades 6-10)'),
        (HIGH_SCHOOL, 'High School (Grades 11-12)'),
    ]

    name = models.CharField(max_length=20, choices=GRADE_CHOICES, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    parent_mobile = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
