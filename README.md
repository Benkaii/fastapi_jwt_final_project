# FastAPI JWT Authentication Calculator

## Final Project Overview

This project is a secure calculator web application built with FastAPI, SQLAlchemy, PostgreSQL, Pydantic, JWT authentication, Docker, Pytest, Playwright, and GitHub Actions.

The application allows authenticated users to perform and save calculations using complete BREAD functionality:

- Browse calculations
- Read calculation details
- Edit existing calculations
- Add new calculations
- Delete calculations

For the final project, the application was extended with a secure **User Profile and Password Management** feature. Authenticated users can view and update their username and email address, securely change their password, and continue using the application with a refreshed JWT token.

The completed project includes automated unit, integration, and Playwright end-to-end tests. The GitHub Actions workflow runs the test suite, performs security checks, builds the Docker image, and pushes the image to Docker Hub.

---

# Features

## Authentication and Security

- User registration
- User login
- JWT access-token authentication
- Protected API routes
- Secure password hashing
- Current-password verification before password changes
- Username and email uniqueness validation
- Pydantic request validation
- User-specific authorization for saved calculations
- Refreshed JWT token after a username change
- Password hashes are never returned through the API

## Calculation BREAD Operations

Authenticated users can manage calculations through the following endpoints:

| Operation | Method | Endpoint | Description |
|---|---|---|---|
| Browse | `GET` | `/calculations` | Retrieve all calculations belonging to the authenticated user |
| Read | `GET` | `/calculations/{id}` | Retrieve one calculation by ID |
| Edit | `PUT` | `/calculations/{id}` | Update an existing calculation |
| Add | `POST` | `/calculations` | Create and save a new calculation |
| Delete | `DELETE` | `/calculations/{id}` | Delete a calculation |

Supported calculation operations include:

- Addition
- Subtraction
- Multiplication
- Division
- Division-by-zero validation

---

# Final Project Feature: User Profile and Password Management

The final project adds a complete profile-management workflow to the existing authenticated calculator application.

Authenticated users can:

- Open the profile page from the calculation dashboard
- View their current username and email address
- View account information
- Update their username
- Update their email address
- Receive a refreshed JWT after changing their username
- Change their password securely
- Verify their current password before setting a new password
- Confirm the new password before submission
- Log out and sign back in using their updated credentials

## Profile API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/profile` | Retrieve the authenticated user's profile |
| `PUT` | `/profile` | Update the authenticated user's username and email |
| `PUT` | `/profile/password` | Verify the current password and securely store a new password |

The profile feature includes positive and negative validation scenarios, including:

- Invalid email addresses
- Duplicate usernames
- Duplicate email addresses
- Incorrect current passwords
- Mismatching new-password confirmation
- Reusing the current password
- Unauthorized requests

---

# Technologies Used

- Python 3.10
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Passlib
- python-jose
- JWT authentication
- Jinja2
- HTML
- CSS
- JavaScript
- Docker
- Docker Compose
- Pytest
- pytest-cov
- Playwright
- GitHub Actions
- Docker Hub

---

# Project Structure

```text
app/
    operations/
        __init__.py
    auth.py
    calculation_factory.py
    crud.py
    database.py
    models.py
    schemas.py
    security.py

.github/
    workflows/
        test.yml

static/
    css/
        style.css
    js/
        auth.js

templates/
    index.html
    login.html
    profile.html
    register.html

tests/
    integration/
        test_calculation_routes.py
        test_calculations.py
        test_fastapi_calculator.py
        test_playwright_auth.py
        test_playwright_profile.py
        test_profile_routes.py
        test_users.py

    unit/
        test_calculation_factory.py
        test_calculation_schemas.py
        test_calculator.py
        test_profile_schemas.py
        test_schemas.py
        test_security.py

    conftest.py

main.py
Dockerfile
docker-compose.yml
pytest.ini
requirements.txt
README.md
```

---

# Running the Application

## Clone the Repository

Clone the GitHub repository:

```bash
git clone https://github.com/Benkaii/fastapi_jwt_final_project.git
```

Enter the project directory:

```bash
cd fastapi_jwt_final_project
```

---

## Run with Docker

Docker Desktop must be running before starting the application with Docker Compose.

Build and start the application:

```bash
docker compose up --build
```

To run the containers in the background:

```bash
docker compose up -d --build
```

View the running containers:

```bash
docker compose ps
```

Stop the application:

```bash
docker compose down
```

Once the containers are running, open:

```text
http://localhost:8000
```

---

## Run Locally

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
venv\Scripts\activate
```

Activate the environment on Linux or macOS:

```bash
source venv/bin/activate
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

The application uses PostgreSQL. Ensure the configured PostgreSQL database is running before starting the application.

Start FastAPI:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

# Application Pages

## Calculation Dashboard

```text
http://localhost:8000/
```

The dashboard provides the authenticated calculation interface and navigation to the profile and logout functionality.

## Registration Page

```text
http://localhost:8000/register-page
```

## Login Page

```text
http://localhost:8000/login-page
```

## User Profile Page

```text
http://localhost:8000/profile-page
```

## Swagger API Documentation

```text
http://localhost:8000/docs
```

## Health Check

```text
http://localhost:8000/health
```

---

# Testing

The project uses Pytest and Playwright to test application logic, API/database integration, authentication, validation, and complete browser workflows.

The final local test suite completed successfully with:

```text
82 passed
Approximately 96% code coverage
```

## Run All Tests

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run the test suite with coverage:

```bash
pytest tests/unit tests/integration --cov=app --cov-fail-under=85 -v
```

The project requires at least 85% code coverage.

---

# Unit Tests

Run the unit tests:

```bash
pytest tests/unit -v
```

Unit tests validate:

- Addition
- Subtraction
- Multiplication
- Division
- Division-by-zero handling
- Calculation factory logic
- Calculation schemas
- User schemas
- Profile schemas
- Password-change schemas
- Invalid email validation
- Password validation
- Password confirmation
- Password hashing
- Password verification

Run the profile-related schema tests:

```bash
pytest tests/unit/test_profile_schemas.py -v
```

---

# Integration Tests

Run the integration tests:

```bash
pytest tests/integration -v
```

Integration tests validate:

- User registration
- User login
- Invalid login attempts
- Duplicate-user protection
- Calculation creation
- Calculation retrieval
- Calculation updates
- Calculation deletion
- Calculation ownership
- Profile retrieval
- Profile updates
- Duplicate username rejection
- Duplicate email rejection
- Invalid email rejection
- Password changes
- Incorrect current-password rejection
- Unauthorized profile access
- Old-password rejection after a password change
- Successful login with the new password

Run the profile integration tests:

```bash
pytest tests/integration/test_profile_routes.py -v
```

---

# Playwright End-to-End Tests

Playwright is used to test the application through a real browser workflow.

Install Playwright:

```bash
pip install playwright
```

Install Chromium:

```bash
python -m playwright install chromium
```

Before running Playwright locally, start the FastAPI application:

```bash
uvicorn main:app --reload
```

Then open a second terminal.

Run the authentication Playwright tests:

```bash
pytest tests/integration/test_playwright_auth.py -v
```

Run the final-project profile Playwright tests:

```bash
pytest tests/integration/test_playwright_profile.py -v
```

To watch the profile tests run in a visible browser:

```bash
pytest tests/integration/test_playwright_profile.py --headed -v
```

## Profile E2E Workflow

The final-project Playwright tests automate the following workflow:

1. Register a new user
2. Log in
3. Open the calculation dashboard
4. Navigate to the profile page
5. Verify the user's profile information
6. Update the user's email address
7. Change the user's password
8. Log out
9. Attempt to log in using the old password
10. Verify that the old password is rejected
11. Log in using the new password
12. Verify that authentication succeeds

Negative Playwright scenarios also verify:

- Mismatching new passwords are rejected
- An incorrect current password is rejected

The final profile E2E test run completed successfully:

```text
3 passed
```

---

# Security

The application implements multiple security controls.

## Password Security

- Passwords are hashed before database storage
- Plaintext passwords are not stored
- Password hashes are not returned through API responses
- The current password must be verified before a password change
- New passwords must satisfy validation requirements
- New-password confirmation must match
- Users cannot reuse their current password

## Authentication and Authorization

- JWT access tokens are used for authentication
- Protected API routes require a valid token
- Profile routes require authentication
- Calculation routes require authentication
- Saved calculations are associated with the authenticated user
- Users cannot access or modify another user's calculations
- Unauthorized requests are rejected

## Profile Security

- Username uniqueness is validated
- Email uniqueness is validated
- Email format is validated
- Password changes require the existing password
- A refreshed JWT is returned when necessary after a profile update

## Deployment Security

- Docker Hub credentials are not stored directly in source code
- GitHub Actions uses encrypted repository secrets
- Docker authentication uses a Docker Hub access token

---

# PostgreSQL and SQLAlchemy

PostgreSQL is used to store application data.

The database stores:

- User accounts
- Usernames
- Email addresses
- Hashed passwords
- Saved calculations
- Calculation operands
- Calculation operation types
- Calculation results
- Calculation ownership

SQLAlchemy provides the application's database layer and is used to:

- Define models
- Create database sessions
- Query users
- Query calculations
- Insert records
- Update records
- Delete records
- Associate calculations with authenticated users

The User Profile and Password Management feature uses fields already available in the user model. Therefore, the final feature did not require a new database table.

Alembic migrations were optional for this assignment and were not necessary for this implementation.

---

# Pydantic Validation

Pydantic schemas are used to validate data entering the API.

Validation includes:

- Registration information
- Login information
- Email format
- Username requirements
- Password requirements
- Password confirmation
- Profile updates
- Password-change requests
- Calculation operands
- Calculation operation types
- Division-by-zero requests

The front end also performs client-side validation and displays success or error messages to the user.

---

# Docker

The application is containerized using Docker.

The project includes:

```text
Dockerfile
docker-compose.yml
```

Docker Compose allows the application and its supporting services to run consistently in containers.

Build the application:

```bash
docker compose build
```

Start it:

```bash
docker compose up
```

Stop it:

```bash
docker compose down
```

---

# Docker Hub

The Docker image is deployed to the following Docker Hub repository:

https://hub.docker.com/r/benkaii/fastapi_calculations

Pull the latest image:

```bash
docker pull benkaii/fastapi_calculations:latest
```

The CI/CD pipeline publishes the latest image after the required test and security stages succeed.

---

# GitHub Actions CI/CD

The GitHub Actions workflow is located at:

```text
.github/workflows/test.yml
```

The automated pipeline contains three primary stages:

```text
test → security → deploy
```

## Test Stage

The workflow:

- Checks out the repository
- Configures Python
- Installs project dependencies
- Configures PostgreSQL for testing
- Installs Playwright and Chromium
- Starts the application when required
- Runs unit tests
- Runs integration tests
- Runs Playwright E2E tests
- Checks code coverage

## Security Stage

The security stage runs automated security checks after the testing requirements are satisfied.

## Deploy Stage

After the required tests and security checks pass, the deployment stage:

- Authenticates to Docker Hub
- Sets up Docker Buildx
- Builds the Docker image
- Pushes the Docker image to Docker Hub

The final GitHub Actions pipeline successfully completed all three stages:

```text
test ✓
security ✓
deploy ✓
```

---

# GitHub Actions Secrets

Docker Hub credentials are stored as encrypted GitHub repository secrets rather than being written directly into the workflow.

The workflow uses:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

The Docker Hub access token is kept outside of the source code and repository.

---

# GitHub Repository

Project repository:

https://github.com/Benkaii/fastapi_jwt_final_project

The repository contains:

- FastAPI application code
- SQLAlchemy database functionality
- Pydantic schemas
- JWT authentication
- BREAD calculation functionality
- User Profile and Password Management functionality
- Front-end templates
- Unit tests
- Integration tests
- Playwright E2E tests
- Docker configuration
- GitHub Actions workflow
- Project documentation

---

# Final Project Results

The completed project demonstrates:

- Complete calculation BREAD functionality
- User-specific calculation storage
- JWT authentication
- Secure password hashing
- Protected API routes
- User Profile Management
- Secure Password Change functionality
- Pydantic validation
- PostgreSQL integration
- SQLAlchemy database operations
- Client-side validation
- Unit testing
- Integration testing
- Playwright E2E testing
- Positive and negative test scenarios
- Approximately 96% code coverage
- 82 passing local tests
- Docker containerization
- Successful GitHub Actions CI/CD
- Successful Docker Hub deployment

---

# Final Project Reflection

This final project brought together many of the concepts I learned throughout Python Web API Development. The project began as a FastAPI calculator application and developed into a complete web application that uses a PostgreSQL database, JWT authentication, password hashing, automated testing, Docker, and a CI/CD pipeline.

For my final project feature, I implemented user profile and password management. An authenticated user can access a profile page, view their current account information, update their username and email address, and securely change their password. Password changes require the user to provide the correct current password. The new password is validated, confirmed, hashed, and stored securely rather than being saved as plaintext.

One important challenge involved handling username changes with JWT authentication. The username is stored in the JWT subject claim, which means the original token would no longer correctly identify the user after a username change. I addressed this by generating and returning a refreshed JWT after a successful profile update. The front end stores the new token so the user can continue using protected routes without being unexpectedly logged out.

Testing was another important part of this project. I created unit tests for the profile and password-change Pydantic schemas, integration tests for the protected profile API routes and database updates, and Playwright end-to-end tests for the complete user workflow. The E2E tests register a user, log in, open the profile page, update account information, change the password, log out, verify that the old password fails, and verify that the new password succeeds. Negative tests also confirm that mismatching passwords, incorrect current passwords, invalid emails, duplicate usernames, duplicate email addresses, and unauthorized requests are handled correctly.

The completed local test suite contains 82 passing tests with approximately 96% code coverage. Reaching this level of coverage helped me understand the importance of testing both successful user workflows and expected failure conditions.

Another major learning experience was implementing the GitHub Actions CI/CD pipeline. Each push automatically runs the test suite and security stage before building and pushing the Docker image to Docker Hub. During development, I encountered and resolved problems involving Playwright timing, HTML selectors, Docker Hub repository secrets, workflow secret names, and Docker authentication. Troubleshooting these issues gave me practical experience reading logs, identifying the actual source of a failure, and verifying fixes locally before pushing them into the automated pipeline.

Docker also helped me better understand how an application, database, and supporting services can run consistently across different systems. Docker Compose simplifies starting the application and supporting services, while the Dockerfile produces a deployable application image.

Overall, this project gave me practical experience creating, securing, testing, containerizing, and deploying a complete Python web application. I gained a much better understanding of how FastAPI routes, Pydantic validation, SQLAlchemy, PostgreSQL, JWT authentication, front-end JavaScript, automated testing, Docker, and GitHub Actions work together as one complete software-development workflow.

---

# Author

**Ismael Albilal**

New Jersey Institute of Technology  
IS 601 – Python Web API Development  
Summer 2026