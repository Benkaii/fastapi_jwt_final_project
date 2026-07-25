# FastAPI JWT Authentication Calculator

## Overview

This project is a secure calculator web application built with FastAPI that implements JWT (JSON Web Token) authentication, PostgreSQL, Docker, Playwright end-to-end testing, Pytest, and GitHub Actions CI/CD.

The application allows users to:

- Register a new account
- Login using JWT authentication
- Store passwords securely using password hashing
- Perform calculator operations
- Store calculation history in PostgreSQL
- Run automated unit, integration, and Playwright end-to-end tests
- Deploy using Docker and Docker Compose

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
.
├── app/
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── login.html
│   └── register.html
│
├── tests/
│   ├── integration/
│   └── unit/
│
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
└── README.md
```

---

# Clone the Repository

```bash
git clone https://github.com/Benkaii/fastapi_jwt_auth.git

cd fastapi_jwt_auth
```

---

# Running the Application

## Build and start Docker containers

```bash
docker compose up --build
```

The application will be available at:

```
http://localhost:8000
```

---

# Front-End Pages

### Registration Page

```
http://localhost:8000/register-page
```

### Login Page

```
http://localhost:8000/login-page
```

### Swagger API Documentation

```
http://localhost:8000/docs
```

---

# Running Unit and Integration Tests

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

---

# Running Playwright End-to-End Tests

Install Playwright:

```bash
pip install playwright
```

Install Playwright browsers:

```bash
python -m playwright install
```

Run the Playwright authentication tests:

```bash
pytest tests/integration/test_playwright_auth.py -v
```

Run with a visible browser:

```bash
pytest tests/integration/test_playwright_auth.py -v --headed
```

The Playwright test suite verifies:

- Successful user registration
- Successful user login
- Invalid login handling
- Password length validation
- Password confirmation validation

---

# Docker Hub Repository

Docker Image:

```
https://hub.docker.com/r/benkaii/fastapi_secure_users
```

---

# GitHub Repository

```
https://github.com/Benkaii/fastapi_jwt_auth
```

---

# Continuous Integration (GitHub Actions)

Every push to the repository automatically performs the following tasks:

- Installs project dependencies
- Builds the Docker image
- Runs Pytest unit and integration tests
- Runs Playwright end-to-end tests
- Pushes the Docker image to Docker Hub after all tests pass

---

# Features

- JWT Authentication
- Secure Password Hashing
- User Registration
- User Login
- Client-side Form Validation
- JWT Token Storage using localStorage
- PostgreSQL Database
- SQLAlchemy ORM
- Docker Support
- Playwright End-to-End Testing
- Pytest Unit Testing
- Pytest Integration Testing
- GitHub Actions CI/CD Pipeline

---

# Screenshots Included

This submission includes:

- Registration page successfully creating a new user
- Login page successfully authenticating a user
- Playwright end-to-end tests passing
- GitHub Actions workflow passing successfully

---

# Reflection

During this project, I implemented JWT authentication into a FastAPI application while integrating PostgreSQL, Docker, Playwright, and GitHub Actions. One of the biggest challenges was troubleshooting Docker networking and database connectivity, particularly ensuring the application communicated correctly with the PostgreSQL container. I also learned how to securely hash passwords, generate and validate JWT tokens, perform client-side validation, and create automated end-to-end tests using Playwright.

The project strengthened my understanding of secure authentication workflows, containerized application deployment, automated testing, and continuous integration. Debugging issues throughout development provided valuable experience with diagnosing application errors, interpreting logs, and systematically resolving configuration problems.

---

# Author

**Ismael Albilal**

New Jersey Institute of Technology

Python Web API Development – Module 13