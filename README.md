# ⚡ Propel AI - Fault Localization System

## Project Overview

This project is a Smart Grid Fault Localization System developed using Django and React.

It simulates IoT devices installed on electricity poles. When a power outage occurs, telemetry is collected, the fault is localized, incidents are created automatically, tickets are generated, and an AI summary is produced.

---

## Features

- Telemetry Ingestion
- Fault Localization
- Incident Management
- Ticket Workflow
- Fault Simulator
- React Dashboard
- AI Incident Summary (Groq)

---

## Technology Stack

### Backend
- Django
- Django REST Framework
- SQLite

### Frontend
- React
- Vite
- Axios

### AI
- Groq API

---

## How to Run

### Backend

```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## API Endpoints

| Method | Endpoint |
|--------|----------|
| POST | /api/telemetry/ |
| POST | /api/inject-fault/ |
| GET | /api/incidents/ |
| GET | /api/tickets/ |
| GET | /api/incidents/<incident_id>/summary/ |

---

## Author

Priya Naik