# LogLens / VulnScan Lite

**A lightweight, on-demand security analysis platform for small businesses, blogs, and developers.**

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![Framework](https://img.shields.io/badge/Framework-FastAPI-green)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 📋 Overview

**LogLens / VulnScan Lite** is a production-ready backend service designed to provide quick security health checks without intrusive penetration testing. It combines passive website scanning and intelligent log analysis to identify potential security vulnerabilities. 

### 🎯 Perfect For: 
- Small businesses needing security monitoring
- Bloggers and content creators
- Developers wanting quick security assessments
- Organizations requiring cost-effective vulnerability detection

---

## ✨ Features

### 1️⃣ **Passive Website Security Scanning**
- HTTPS/SSL enforcement verification
- Security header detection and analysis
  - Content-Security-Policy (CSP)
  - X-Frame-Options
  - X-Content-Type-Options
  - Strict-Transport-Security (HSTS)
- Server information exposure detection
- HTTP status code validation
- Risk scoring (LOW/MEDIUM/HIGH)

### 2️⃣ **Log File Threat Analysis**
- Brute-force attack detection
- SQL injection pattern matching
- XSS (Cross-Site Scripting) detection
- Suspicious activity identification
- IP frequency analysis
- Authentication failure tracking
- Threat density calculation

### 3️⃣ **Comprehensive Reporting**
- Structured JSON responses
- Threat breakdown by category
- Detailed security findings
- Actionable recommendations
- Scan history management

### 4️⃣ **Free vs Premium Tiers**
- **Free Tier**: Limited threat details, basic insights
- **Premium Tier**: Full threat visibility, detailed analysis, premium insights
- Logic-level separation (no payment gateway required)

### 5️⃣ **Production-Ready API**
- RESTful endpoints with Swagger UI
- Request/response validation (Pydantic)
- Comprehensive error handling
- Structured logging
- Database persistence (SQLite)

---

## 📁 Project Structure

```
backend/
│
├── app/
│   ├── main.py                          # FastAPI application entry point
│   ├── config.py                        # Environment configuration & settings
│   │
│   ├── api/
│   │   └── routes.py                    # All API endpoints (v1)
│   │
│   ├── core/
│   │   ├── scanner.py                   # Scan dispatcher & orchestration
│   │   └── analyzer.py                  # Threat analysis & enrichment
│   │
│   ├── services/
│   │   ├── url_scan.py                  # URL security scanning logic
│   │   └── log_scan.py                  # Log file threat detection
│   │
│   ├── models/
│   │   ├── schemas.py                   # Pydantic request/response models
│   │   ├── database.py                  # SQLAlchemy setup & session mgmt
│   │   └── tables.py                    # Database ORM models
│   │
│   ├── utils/
│   │   └── helpers.py                   # Utility functions
│   │
│   └── logs/                            # Application logs directory
│
├── requirements.txt                     # Python dependencies
├── . env. example                         # Example environment variables
└── README.md                            # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### 1. Clone or Download Project

```bash
# If from GitHub
git clone https://github.com/yourusername/vulnscan-lite.git
cd vulnscan-lite/backend

# Or extract from zip file
cd backend
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the `backend` directory:

```bash
# Copy the example (if provided)
cp .env.example .env

# Or create manually
touch .env
```

**Example `.env` file:**
```
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Database
DATABASE_URL=sqlite:///./security_scans.db

# HTTP Configuration
HTTP_TIMEOUT=10
HTTP_MAX_RETRIES=2

# Logging
LOG_LEVEL=INFO
LOG_DIR=app/logs

# Features
ENABLE_HISTORY=True
```

### 5. Run the Backend

```bash
# Start development server
python -m app.main

# Or directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
2026-01-15 10:30:00 - app.main - INFO - 🚀 Starting LogLens/VulnScan Lite Backend
2026-01-15 10:30:00 - app.main - INFO - ✅ Database tables initialized
INFO:     Application startup complete [uvicorn]
```

### 6. Access the API

- **API