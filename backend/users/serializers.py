from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentProfile, GradeLevel

class GradeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeLevel
        fields = ['id', 'name', 'description']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    grade_level = GradeLevelSerializer(read_only=True)
    grade_level_id = serializers.PrimaryKeyRelatedField(
        queryset=GradeLevel.objects.all(),
        source='grade_level',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'student_id', 'grade_level', 'grade_level_id', 
            'date_of_birth', 'parent_mobile', 'profile_picture', 
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']

class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    student_id = serializers.CharField(required=True)
    grade_level_id = serializers.PrimaryKeyRelatedField(
        queryset=GradeLevel.objects.all(),
        required=False
    )
    date_of_birth = serializers.DateField(required=False)
    parent_mobile = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 
            'first_name', 'last_name', 'student_id', 'grade_level_id',
            'date_of_birth', 'parent_mobile'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        grade_level = validated_data.pop('grade_level_id', None)
        date_of_birth = validated_data.pop('date_of_birth', None)
        parent_mobile = validated_data.pop('parent_mobile', '')
        password_confirm = validated_data.pop('password_confirm')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        StudentProfile.objects.create(
            user=user,
            student_id=student_id,
            grade_level=grade_level,
            date_of_birth=date_of_birth,
            parent_mobile=parent_mobile
        )
        
        return user

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password_confirm = serializers.CharField(required=True, style={'input_type': 'password'})
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "New passwords do not match."})
        return data
