import os
import django
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rural_education_app.settings')
django.setup()

from assessment.models import Assessment, Question, Answer
from content.models import Subject, GradeLevel

def create_test_data():
    """Create test data for the assessment app."""
    print("Creating test data for the assessment app...")
    
    # Create subjects if they don't exist
    math_subject, _ = Subject.objects.get_or_create(
        name='Mathematics',
        defaults={'description': 'Mathematics for elementary students'}
    )
    
    # Create grade levels if they don't exist
    grade1, _ = GradeLevel.objects.get_or_create(
        name='Grade 1',
        defaults={'description': 'First grade elementary level'}
    )
    
    # Create assessments for each difficulty level
    difficulty_levels = ['easy', 'moderate', 'hard']
    
    for difficulty in difficulty_levels:
        assessment, created = Assessment.objects.get_or_create(
            title=f'Grade 1 Numbers and Operations - {difficulty.capitalize()}',
            defaults={
                'description': f'Practice test for Grade 1 students on numbers and operations ({difficulty} difficulty).',
                'subject': math_subject,
                'grade_level': grade1,
                'assessment_type': 'practice',
                'difficulty': difficulty,
                'time_limit_minutes': 20,
                'passing_score': 70,
                'is_active': True
            }
        )
        
        if created:
            print(f"Created assessment: {assessment.title}")
        else:
            print(f"Assessment already exists: {assessment.title}")
            continue
        
        # Create questions for each assessment
        num_questions = 10
        
        for i in range(1, num_questions + 1):
            # Adjust question difficulty based on the assessment difficulty
            if difficulty == 'easy':
                num1, num2 = i, i + 1
                operation = '+'
                answer = num1 + num2
            elif difficulty == 'moderate':
                num1, num2 = i * 2, i
                operation = '-'
                answer = num1 - num2
            else:  # hard
                num1, num2 = i, 2
                operation = '×'
                answer = num1 * num2
            
            question_text = f"{i}. What is {num1} {operation} {num2}?"
            
            # Create the question
            question = Question.objects.create(
                assessment=assessment,
                text=question_text,
                question_type='multiple_choice',
                points=1
            )
            
            # Create answers (1 correct, 3 incorrect)
            Answer.objects.create(
                question=question,
                text=str(answer),
                is_correct=True
            )
            
            # Create incorrect answers
            incorrect_answers = [answer + 1, answer - 1, answer + 2]
            if 0 in incorrect_answers:  # Avoid zero as an answer for young students
                incorrect_answers = [answer + 1, answer + 2, answer + 3]
            
            for incorrect in incorrect_answers:
                if incorrect != answer and incorrect > 0:  # Ensure positive numbers
                    Answer.objects.create(
                        question=question,
                        text=str(incorrect),
                        is_correct=False
                    )
        
        print(f"Created {num_questions} questions for {assessment.title}")

if __name__ == '__main__':
    create_test_data()
    print("Test data creation completed!")
