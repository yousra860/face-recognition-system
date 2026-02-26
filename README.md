# 🔐 Face Recognition Cloud System

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8-orange.svg)](https://opencv.org)

**Master 2 RISR - Final Year Project**  
**Université de Saida - Dr. Moulay Tahar**

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Screenshots](#screenshots)
- [Team](#team)

---

## ✨ Features

### Core Features
- ✅ **Face Enrollment**: Register new faces with personal information
- ✅ **1:1 Verification**: Verify identity against specific user
- ✅ **1:N Identification**: Search database for matching faces
- ✅ **Real-time Processing**: Fast face detection and recognition
- ✅ **JWT Authentication**: Secure login system
- ✅ **Web Interface**: User-friendly responsive design
- ✅ **Camera Support**: Direct capture from webcam

### Technical Features
- 🚀 **FastAPI**: High-performance async backend
- 🎯 **OpenCV**: Computer vision and face recognition
- 🗄️ **SQLAlchemy**: Database ORM with SQLite/PostgreSQL
- 🔒 **Security**: Password hashing, JWT tokens, CORS
- 🐳 **Docker**: Containerized deployment ready
- 📊 **Monitoring**: Health checks and metrics

---

## 🚀 Quick Start

### Option 1: Using the run script
```bash
./run.sh
### Option 2: Manual setup
# 1. Activate virtual environment
source venv/bin/activate

# 2. Start server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
