# Deployment Guide

## Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create a `.env` file in the backend:

```env
GROQ_API_KEY=your_groq_api_key
```

## Deployment

The application can be deployed using:

- Render
- Railway
- Docker Compose

## Services

- Backend: Django
- Frontend: React (Vite)
- Database: SQLite
- AI: Groq