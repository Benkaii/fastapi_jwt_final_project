# FastAPI JWT Authentication Calculator

## Overview

This project is a secure calculator web application built using FastAPI that implements JWT (JSON Web Token) authentication, PostgreSQL, Docker, Playwright end-to-end testing, Pytest, and GitHub Actions CI/CD.

The application allows authenticated users to:

- Register a new account
- Login using JWT authentication
- Securely hash passwords
- Perform calculator operations
- Create, Browse, Read, Edit, and Delete calculations (BREAD)
- Store user-specific calculations in PostgreSQL
- Run automated unit, integration, and Playwright tests
- Build and deploy using Docker
- Automatically test and deploy using GitHub Actions

---

# Technologies Used

- Python 3.10
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Passlib
- python-jose (JWT)
- Docker
- Docker Compose
- Pytest
- Playwright
- GitHub Actions

---

# Project Structure

```
app/
    auth.py
    crud.py
    database.py
    models.py
    schemas.py
    security.py

static/
    css/
    js/

templates/
    login.html
    register.html

tests/
    unit/
    integration/

main.py
Dockerfile
docker-compose.yml
requirements.txt
README.md
```

---

# Clone the Repository

```bash
git clone https://github.com/Benkaii/fastapi_jwt_auth.git

cd fastapi_jwt_auth
```

---

# Running the Application

Build and start the application using Docker.

```bash
docker compose up --build
```

Once the containers finish building, open:

```
http://localhost:8000
```

---

# Application Pages

Registration Page

```
http://localhost:8000/register-page
```

Login Page

```
http://localhost:8000/login-page
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

# Running Tests

Run all tests

```bash
pytest
```

Verbose output

```bash
pytest -v
```

---

# Running Playwright Tests

Install Playwright

```bash
pip install playwright
```

Install browser

```bash
python -m playwright install
```

Run Playwright tests

```bash
pytest tests/integration/test_playwright_auth.py -v
```

Run in headed mode

```bash
pytest tests/integration/test_playwright_auth.py --headed -v
```

Playwright verifies:

- User Registration
- User Login
- Invalid Login
- Password Validation
- BREAD functionality

---

# Docker Hub Repository

https://hub.docker.com/r/benkaii/fastapi_calculations

---

# GitHub Repository

https://github.com/Benkaii/fastapi_jwt_auth

---

# GitHub Actions

Every push automatically:

- Installs project dependencies
- Builds the Docker image
- Runs unit tests
- Runs integration tests
- Runs Playwright end-to-end tests
- Pushes the Docker image to Docker Hub

---

# Features

- JWT Authentication
- Secure Password Hashing
- User Registration
- User Login
- Browse Calculations
- Read Calculation Details
- Add Calculations
- Edit Calculations
- Delete Calculations
- Client-side Validation
- PostgreSQL Database
- SQLAlchemy ORM
- Docker Support
- Playwright End-to-End Testing
- Pytest Unit Testing
- Pytest Integration Testing
- GitHub Actions CI/CD

---

# Included Screenshots

This submission contains screenshots demonstrating:

- User Registration
- User Login
- Add Calculation
- Read Calculation
- Edit Calculation
- Delete Calculation
- GitHub Actions workflow
- Docker Hub deployment

---

# Author

**Ismael Albilal**

New Jersey Institute of Technology

IS 601 – Python Web API Development

Summer 2026