import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rural_education_app.settings')
django.setup()

from assessment.models import Assessment, Question, Answer
from content.models import Subject, GradeLevel

def create_test_questions():
    """Create test questions for the application."""
    # Get or create the Mathematics subject
    math_subject, _ = Subject.objects.get_or_create(
        name='Mathematics',
        defaults={'description': 'Mathematics for elementary students'}
    )

    # Get or create the Grade 1 level
    grade1, _ = GradeLevel.objects.get_or_create(
        name='Grade 1',
        defaults={'description': 'First grade elementary level'}
    )

    # Create assessments for each difficulty level
    difficulty_levels = ['easy', 'moderate', 'hard']

    for difficulty in difficulty_levels:
        # Create an assessment for this difficulty level
        assessment, created = Assessment.objects.get_or_create(
            title=f'Grade 1 Numbers and Operations - {difficulty.capitalize()}',
            defaults={
                'description': f'Practice test for Grade 1 students on numbers and operations ({difficulty} difficulty).',
                'subject': math_subject,
                'grade_level': grade1,
                'assessment_type': 'practice',
                'difficulty': difficulty,
                'time_limit_minutes': 20,
                'passing_score': 70
            }
        )

        if created:
            print(f"Created assessment: {assessment.title}")
        else:
            print(f"Assessment already exists: {assessment.title}")
            continue

        # Create questions for each assessment
        questions_data = []

        if difficulty == 'easy':
            questions_data = [
                {
                    'text': '1. What is 1 + 1?',
                    'answers': [
                        {'text': 'A) 1', 'is_correct': False},
                        {'text': 'B) 2', 'is_correct': True},
                        {'text': 'C) 3', 'is_correct': False},
                        {'text': 'D) 4', 'is_correct': False}
                    ]
                },
                {
                    'text': '2. What is 2 + 1?',
                    'answers': [
                        {'text': 'A) 2', 'is_correct': False},
                        {'text': 'B) 3', 'is_correct': True},
                        {'text': 'C) 4', 'is_correct': False},
                        {'text': 'D) 5', 'is_correct': False}
                    ]
                },
                {
                    'text': '3. What is 2 + 2?',
                    'answers': [
                        {'text': 'A) 3', 'is_correct': False},
                        {'text': 'B) 4', 'is_correct': True},
                        {'text': 'C) 5', 'is_correct': False},
                        {'text': 'D) 6', 'is_correct': False}
                    ]
                },
                {
                    'text': '4. What is 3 + 1?',
                    'answers': [
                        {'text': 'A) 3', 'is_correct': False},
                        {'text': 'B) 4', 'is_correct': True},
                        {'text': 'C) 5', 'is_correct': False},
                        {'text': 'D) 6', 'is_correct': False}
                    ]
                },
                {
                    'text': '5. What is 2 + 3?',
                    'answers': [
                        {'text': 'A) 4', 'is_correct': False},
                        {'text': 'B) 5', 'is_correct': True},
                        {'text': 'C) 6', 'is_correct': False},
                        {'text': 'D) 7', 'is_correct': False}
                    ]
                },
                {
                    'text': '6. What is 3 + 2?',
                    'answers': [
                        {'text': 'A) 4', 'is_correct': False},
                        {'text': 'B) 5', 'is_correct': True},
                        {'text': 'C) 6', 'is_correct': False},
                        {'text': 'D) 7', 'is_correct': False}
                    ]
                },
                {
                    'text': '7. What is 4 + 1?',
                    'answers': [
                        {'text': 'A) 4', 'is_correct': False},
                        {'text': 'B) 5', 'is_correct': True},
                        {'text': 'C) 6', 'is_correct': False},
                        {'text': 'D) 7', 'is_correct': False}
                    ]
                },
                {
                    'text': '8. Count the objects: ○○○. How many are there?',
                    'answers': [
                        {'text': 'A) 2', 'is_correct': False},
                        {'text': 'B) 3', 'is_correct': True},
                        {'text': 'C) 4', 'is_correct': False},
                        {'text': 'D) 5', 'is_correct': False}
                    ]
                },
                {
                    'text': '9. Count the objects: ○○○○. How many are there?',
                    'answers': [
                        {'text': 'A) 3', 'is_correct': False},
                        {'text': 'B) 4', 'is_correct': True},
                        {'text': 'C) 5', 'is_correct': False},
                        {'text': 'D) 6', 'is_correct': False}
                    ]
                },
                {
                    'text': '10. What number comes after 4?',
                    'answers': [
                        {'text': 'A) 3', 'is_correct': False},
                        {'text': 'B) 5', 'is_correct': True},
                        {'text': 'C) 6', 'is_correct': False},
                        {'text': 'D) 7', 'is_correct': False}
                    ]
                }
            ]
        elif difficulty == 'moderate':
            questions_data = [
                {
                    'text': '1. What is 5 + 7?',
                    'answers': [
                        {'text': 'A) 11', 'is_correct': False},
                        {'text': 'B) 12', 'is_correct': True},
                        {'text': 'C) 13', 'is_correct': False},
                        {'text': 'D) 14', 'is_correct': False}
                    ]
                },
                {
                    'text': '2. What is 10 - 4?',
                    'answers': [
                        {'text': 'A) 5', 'is_correct': False},
                        {'text': 'B) 6', 'is_correct': True},
                        {'text': 'C) 7', 'is_correct': False},
                        {'text': 'D) 8', 'is_correct': False}
                    ]
                },
                {
                    'text': '3. If you have 3 apples and get 5 more, how many apples do you have?',
                    'answers': [
                        {'text': 'A) 7', 'is_correct': False},
                        {'text': 'B) 8', 'is_correct': True},
                        {'text': 'C) 9', 'is_correct': False},
                        {'text': 'D) 10', 'is_correct': False}
                    ]
                }
            ]
        elif difficulty == 'hard':
            questions_data = [
                {
                    'text': '1. What is 8 + 9?',
                    'answers': [
                        {'text': 'A) 16', 'is_correct': False},
                        {'text': 'B) 17', 'is_correct': True},
                        {'text': 'C) 18', 'is_correct': False},
                        {'text': 'D) 19', 'is_correct': False}
                    ]
                },
                {
                    'text': '2. What is 15 - 7?',
                    'answers': [
                        {'text': 'A) 7', 'is_correct': False},
                        {'text': 'B) 8', 'is_correct': True},
                        {'text': 'C) 9', 'is_correct': False},
                        {'text': 'D) 10', 'is_correct': False}
                    ]
                },
                {
                    'text': '3. If you have 12 candies and give 5 to your friend, how many do you have left?',
                    'answers': [
                        {'text': 'A) 6', 'is_correct': False},
                        {'text': 'B) 7', 'is_correct': True},
                        {'text': 'C) 8', 'is_correct': False},
                        {'text': 'D) 9', 'is_correct': False}
                    ]
                }
            ]

        # Create the questions and answers
        for i, q_data in enumerate(questions_data):
            # Create the question
            question = Question.objects.create(
                assessment=assessment,
                question_text=q_data['text'],
                question_type='multiple_choice',
                points=1,
                order=i+1
            )

            # Create the answers
            for j, a_data in enumerate(q_data['answers']):
                Answer.objects.create(
                    question=question,
                    answer_text=a_data['text'],
                    is_correct=a_data['is_correct'],
                    order=j+1
                )

            print(f"Created question: {question.question_text}")

        print(f"Created {len(questions_data)} questions for {assessment.title}")

if __name__ == '__main__':
    create_test_questions()
