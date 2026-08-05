# System Architecture

## Overview

The system consists of four major components:

1. React Dashboard
2. Django REST API
3. SQLite Database
4. Groq AI

---

## Architecture Flow

React Dashboard

↓

REST API (Django)

↓

Fault Localization Engine

↓

Incident Manager

↓

Ticket Manager

↓

SQLite Database

↓

Groq AI Summary

---

## Fault Localization

Telemetry from IoT devices is received by the backend.

The algorithm:

- Orders poles by sequence number
- Finds the last energized pole
- Finds the first de-energized pole
- Identifies the fault boundary
- Creates one incident
- Prevents duplicate incidents

---

## AI

Groq generates a short natural-language summary for each detected incident.

---

## Future Improvements

- GPS-based localization
- Real-time WebSocket updates
- Transformer topology inference
- Map visualization
- Multi-feeder support