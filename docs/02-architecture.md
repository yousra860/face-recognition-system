# Chapter 2: System Architecture

## 2.1 Overview

## 2.2 Components

### Frontend (HTML/CSS/JS)
- Responsive design
- Camera integration
- Real-time feedback

### Backend (FastAPI)
- RESTful API
- JWT authentication
- Async processing

### Face Recognition (OpenCV)
- Haar Cascade detection
- LBPH recognition
- 128-dimensional encoding

### Database (SQLAlchemy)
- User management
- Face templates
- Access logs

## 2.3 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/v1/auth/login | POST | User authentication |
| /api/v1/enroll/ | POST | Register new face |
| /api/v1/verify/ | POST | Verify identity (1:1) |
| /api/v1/identify/ | POST | Identify person (1:N) |

## 2.4 Security

- JWT tokens for authentication
- Password hashing (bcrypt)
- HTTPS ready
- CORS protection
