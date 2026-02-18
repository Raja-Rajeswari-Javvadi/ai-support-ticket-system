AI Support Ticket Classification System

Architecture:

Frontend:
- HTML + JavaScript interface inside Django templates

Backend:
- Django REST Framework
- Ticket CRUD APIs
- Stats API

AI Layer:
- Google Gemini (gemini-2.5-flash)
- Prompt-based classification

Flow:
User → UI → Django API → Gemini → Response → DB → UI

Database:
- SQLite (can be swapped to PostgreSQL)

Key Features:
- Auto ticket categorization
- Auto priority detection
- Search & filter tickets
- Ticket statistics dashboard
