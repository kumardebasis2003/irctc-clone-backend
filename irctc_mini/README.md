# 🚂 IRCTC Mini System - Backend API

Production-ready Django REST Framework backend for train booking system with JWT authentication and PostgreSQL database.

## ✨ Features
- 🔐 JWT-based authentication with token blacklist
- 🚉 Train management (CRUD operations - Admin only)
- 🎫 Booking system with seat validation
- 📊 Real-time seat availability tracking
- 👥 Role-based access control (User/Admin)
- 📱 RESTful API with Swagger documentation
- ✅ PostgreSQL database (No MongoDB dependency)

## 🛠️ Tech Stack
- **Framework**: Django 4.2+
- **API**: Django REST Framework 3.14+
- **Authentication**: Simple JWT
- **Database**: PostgreSQL 12+
- **API Docs**: Swagger (drf-yasg)
- **Security**: CORS headers, Token blacklist

## 📋 Prerequisites
- Python 3.10+
- PostgreSQL 12+
- pip package manager
- Virtual environment (venv)

## 🚀 Setup Instructions

### 1. Clone and Setup Environment
```bash
# Create project directory
mkdir irctc_mini && cd irctc_mini

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt