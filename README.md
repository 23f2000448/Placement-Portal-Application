# Placement Portal Application V2

A full-stack campus recruitment platform that streamlines the placement process between **Students**, **Companies**, and **Placement Administrators**.

The application provides a centralized system for managing job postings, student applications, interview scheduling, placement records, and recruitment analytics while enforcing role-based access control and approval workflows.

---

## Features

### Authentication & Authorization

* JWT-based authentication
* Role-based access control (Admin, Company, Student)
* Student self-registration
* Company registration with admin approval workflow
* Secure login and session management
* Protected dashboard routes

### Student Portal

* Student profile management
* Education and skills tracking
* Resume management
* Browse and search job opportunities
* Apply for placement drives
* Track application status
* View interview schedules
* Download offer letters and placement confirmations

### Company Portal

* Company profile registration
* Admin approval workflow
* Create and manage job postings
* Review applications
* Shortlist and reject candidates
* Schedule interviews
* Manage placement drive status
* Publish hiring decisions

### Admin Portal

* Platform-wide dashboard
* Company approval and management
* Student management
* Job posting moderation
* Application monitoring
* User deactivation and blacklisting
* Placement statistics overview

### Placement Management

* Placement drive creation
* Application lifecycle management
* Interview scheduling
* Placement record tracking
* Offer management

### Background Processing

* Interview reminder jobs
* Placement report generation
* CSV export processing
* Scheduled analytics tasks

### Performance Optimization

* Redis-based caching
* Optimized API responses
* Asynchronous background workers using Celery

---

## Architecture

```text
placement-portal-v2/
├── backend/
│   ├── app/
│   │   ├── models/              # SQLAlchemy database models
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic layer
│   │   ├── schemas/             # Marshmallow validation schemas
│   │   ├── tasks/               # Celery background jobs
│   │   ├── utils/               # Utility functions
│   │   ├── extensions.py        # Flask extensions
│   │   └── config.py            # Application configuration
│   │
│   ├── migrations/             # Database migrations
│   ├── seed.py                 # Initial admin seeding
│   ├── run.py                  # Application entry point
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── router/
│   │   ├── stores/
│   │   ├── services/
│   │   └── assets/
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Tech Stack

| Layer               | Technology  |
| ------------------- | ----------- |
| **Frontend**        | Vue.js      |
| **Backend**         | Flask       |
| **Language**        | Python      |
| **Database**        | SQLite      |
| **ORM**             | SQLAlchemy  |
| **Authentication**  | JWT         |
| **Validation**      | Marshmallow |
| **Caching**         | Redis       |
| **Background Jobs** | Celery      |
| **API Style**       | REST API    |

---

## Core Database Models

### User

Supports three system roles:

* Admin
* Company
* Student

### Student

* Personal information
* Education details
* Skills
* Resume
* Placement history

### Company

* Company profile
* Industry
* Location
* Approval status

### Job Position

* Position title
* Job description
* Salary package
* Required skills
* Eligibility criteria

### Application

* Student association
* Job association
* Application status
* Application timestamps

### Interview

* Scheduled interviews
* Interview feedback
* Selection outcomes

### Placement

* Final placement records
* Salary package
* Joining details

---

## Application Workflow

```text
Student Registration
        │
        ▼
Profile Completion
        │
        ▼
Browse Job Opportunities
        │
        ▼
Apply for Position
        │
        ▼
Application Review
        │
        ▼
Shortlisted
        │
        ▼
Interview Scheduled
        │
        ▼
Selected / Rejected
        │
        ▼
Placement Record Created
```

---

## API Modules

### Authentication

```http
POST /api/auth/register/student
POST /api/auth/register/company
POST /api/auth/login
POST /api/auth/logout
```

### Students

```http
GET    /api/students/profile
PUT    /api/students/profile
GET    /api/students/applications
```

### Companies

```http
GET    /api/companies/profile
PUT    /api/companies/profile
GET    /api/companies/jobs
POST   /api/companies/jobs
PATCH  /api/companies/jobs/:id
```

### Job Positions

```http
GET    /api/jobs
GET    /api/jobs/:id
POST   /api/jobs
PATCH  /api/jobs/:id
DELETE /api/jobs/:id
```

### Applications

```http
POST   /api/applications
GET    /api/applications
PATCH  /api/applications/:id
```

### Placements

```http
GET    /api/placements
POST   /api/placements
```

---

## Milestone Roadmap

### Core Requirements

* [ ] Database Models and Schema Setup
* [ ] Authentication and Role-Based Access
* [ ] Admin Dashboard and Management
* [ ] Company Dashboard and Job Management
* [ ] Student Dashboard and Application System
* [ ] Application History and Status Tracking
* [ ] Celery Background Jobs and Reports
* [ ] Redis Caching and API Optimization

### Recommended Enhancements

* [ ] Progressive Web App (PWA)
* [ ] Mobile Responsive Design
* [ ] Placement Analytics Dashboard
* [ ] ATS Resume Screening
* [ ] Public Placement Statistics Dashboard

---

## Local Development

### Prerequisites

* Python 3.10+
* Node.js 18+
* Redis
* npm

---

### Backend Setup

```bash
cd backend

python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

python run.py
```

Backend runs on:

```text
http://localhost:5000
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

### Redis Setup

```bash
redis-server
```

---

### Celery Worker

```bash
celery -A app.celery worker --loglevel=info
```

---

## Future Enhancements

* Resume ATS Scoring
* Email Notification System
* Real-Time Updates
* Placement Analytics Dashboard
* Docker Deployment
* CI/CD Pipeline
* Cloud Storage Integration
* Multi-Institute Support

---

## Security Considerations

* JWT-based authentication
* Password hashing using Werkzeug security utilities
* Protected API routes
* Role-based authorization
* Input validation using Marshmallow schemas
* Secure company approval workflow

---

## Project Status

🚧 **Active Development**

This project is being developed as part of the **Modern Application Development II (MAD-II)** course and follows a milestone-driven roadmap covering authentication, placement management, reporting, caching, analytics, and deployment.

---

## Author

**Tanuj Nain**

Placement Portal Application V2
Modern Application Development II (MAD-II)
