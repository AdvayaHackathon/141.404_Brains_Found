# Rural Education App

A web-based educational platform designed for students in rural areas with limited internet connectivity. The application provides educational content for elementary students (grades 1-5) with features like offline access, grade-based content filtering, and an AI assistant for answering questions.

## Features

- **User Authentication**: Student registration, login, and profile management
- **Grade-Based Content**: Educational materials tailored for grades 1-5
- **Teaching Module**: Organized lessons by subject with downloadable content for offline access
- **Testing Module**: Practice tests, quizzes, and graded exams with performance tracking
- **Offline AI Bot**: Lightweight AI assistant that can answer educational questions
- **Responsive Design**: Works on various devices including low-end mobile phones

## Technology Stack

### Frontend
- React.js with Vite
- React Router for navigation
- Bootstrap 5 for responsive UI
- Axios for API communication

### Backend
- Django web framework
- Django REST Framework for API
- SQLite database (can be upgraded to PostgreSQL for production)
- Token-based authentication

## Getting Started

### Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- npm or yarn

### Installation

#### Backend Setup
1. Navigate to the backend directory:
   ```
   cd rural-education-app/backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

#### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd rural-education-app/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

## Project Structure

```
rural-education-app/
├── backend/                # Django backend
│   ├── ai_assistant/       # AI assistant app
│   ├── assessment/         # Testing module app
│   ├── content/            # Teaching module app
│   ├── users/              # User authentication app
│   └── rural_education_app/# Django project settings
├── frontend/               # React frontend
│   ├── public/             # Static files
│   └── src/                # Source files
│       ├── components/     # React components
│       ├── context/        # Context providers
│       └── services/       # API services
└── README.md               # Project documentation
```

## Offline Functionality

The application is designed to work in environments with limited internet connectivity:

1. **Downloadable Content**: Lessons can be downloaded for offline access
2. **Lightweight AI**: The AI assistant uses a compressed model that can run in the browser
3. **Service Workers**: Static assets are cached for offline use
4. **Local Storage**: User progress is stored locally and synced when online

## License

This project is licensed under the MIT License - see the LICENSE file for details.
