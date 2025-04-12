import os
import sys
import django
import docx
import re

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rural_education_app.settings')
django.setup()

from assessment.models import Assessment, Question, Answer
from content.models import Subject, GradeLevel

def extract_questions_from_docx(file_path):
    """Extract questions and answers from a Word document."""
    doc = docx.Document(file_path)
    questions = []
    current_question = None
    current_answers = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Check if this is a question (starts with a number followed by a period or parenthesis)
        question_match = re.match(r'^\d+[\.\)]', text)
        if question_match:
            # If we already have a question, save it before starting a new one
            if current_question:
                questions.append({
                    'question_text': current_question,
                    'answers': current_answers
                })

            # Start a new question
            current_question = text
            current_answers = []
        elif text.startswith(('a)', 'b)', 'c)', 'd)', 'A)', 'B)', 'C)', 'D)')):
            # This is an answer option
            is_correct = '*' in text  # Assuming correct answers are marked with an asterisk
            answer_text = text.replace('*', '').strip()
            current_answers.append({
                'text': answer_text,
                'is_correct': is_correct
            })

    # Don't forget to add the last question
    if current_question:
        questions.append({
            'question_text': current_question,
            'answers': current_answers
        })

    return questions

def import_questions_from_notes():
    """Import questions from the notes directory."""
    # Define the path to the notes directory
    notes_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'notes')

    # Check if the directory exists
    if not os.path.exists(notes_dir):
        print(f"Notes directory not found: {notes_dir}")
        return

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

    # Process each difficulty level
    difficulty_files = {
        'easy': 'Numbers-and-operations.docx',
        'moderate': 'Numbers-and-operations-moderate.docx',
        'hard': 'Numbers-and-operations-hard.docx'
    }

    for difficulty, filename in difficulty_files.items():
        file_path = os.path.join(notes_dir, filename)

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

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
            # Skip if we've already processed this assessment
            continue

        # Extract questions from the document
        try:
            questions_data = extract_questions_from_docx(file_path)

            for q_data in questions_data:
                # Create the question
                question = Question.objects.create(
                    assessment=assessment,
                    text=q_data['question_text'],
                    question_type='multiple_choice',
                    points=1
                )

                # Create the answers
                for a_data in q_data['answers']:
                    Answer.objects.create(
                        question=question,
                        text=a_data['text'],
                        is_correct=a_data['is_correct']
                    )

            print(f"Imported {len(questions_data)} questions for {assessment.title}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == '__main__':
    import_questions_from_notes()
