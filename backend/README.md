# DeepLogic Backend API

This is the backend API for the DeepLogic application, providing authentication and issue management functionality. The application supports role-based access control with three user roles: Admin, Maintainer, and Reporter.

## Project Overview

DeepLogic is a Django-based issue tracking system that allows:
- Reporters to submit and track issues
- Maintainers to triage and update issue status
- Admins to manage the entire system

## Technologies Used

- **Backend Framework**: Django 4.2 with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: 
  - Token-based authentication
  - Google OAuth2 for reporters
  - Email/password for maintainers and admins
- **Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Containerization**: Docker

## Table of Contents
- [Project Structure](#project-structure)
- [Authentication](#authentication)
  - [Email/Password Login](#emailpassword-login)
  - [Google OAuth2](#google-oauth2)
  - [Get Current User](#get-current-user)
- [Issues](#issues)
  - [Create Issue](#create-issue)
  - [List Issues](#list-issues)
  - [Get Issue](#get-issue)
  - [Update Issue Status/Severity](#update-issue-statusseverity)
  - [Delete Issue](#delete-issue)
  - [Issue Statistics](#issue-statistics)
- [User Management](#user-management)

## Authentication

### Email/Password Login
Used by maintainers/admins to log in with email and password.

**Endpoint**: `POST /api/auth/login/`

**Request Body**:
```json
{
  "email": "admin@example.com",
  "password": "yourpassword"
}
```

**Response**:
```json
{
  "token": "your_auth_token",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  }
}
```

### Google OAuth2
Used by reporters to authenticate using Google OAuth2.

1. **Initiate OAuth Flow**:
   - Redirect users to: `GET /auth/login/google-oauth2/`

2. **OAuth Callback**:
   - **Endpoint**: `GET /auth/complete/google-oauth2/`
   - **Response**:
     ```json
     {
       "token": "your_auth_token",
       "user": {
         "id": 2,
         "username": "user123",
         "email": "user@example.com"
       },
       "is_new_user": true
     }
     ```

### Get Current User
Get details of the currently authenticated user.

**Endpoint**: `GET /api/auth/user/`

**Headers**:
```
Authorization: Token your_auth_token
```

**Response**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com"
}
```

## Issues

### Create Issue
Create a new issue. Can include file attachments.

**Endpoint**: `POST /api/issues/create/`

**Headers**:
```
Authorization: Token your_auth_token
Content-Type: multipart/form-data
```

**Form Data**:
- `title` (string, required): Issue title
- `description` (string, required): Detailed description
- `severity` (string, optional): One of [LOW, MEDIUM, HIGH, CRITICAL], defaults to MEDIUM
- `attachment` (file, optional): Attached file

**Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Bug in login page",
  "description": "The login button doesn't work on mobile",
  "status": "OPEN",
  "severity": "HIGH",
  "created_by": 2,
  "created_at": "2023-07-04T12:00:00Z",
  "updated_at": "2023-07-04T12:00:00Z"
}
```

### List Issues
Get a list of all issues. Regular users only see their own issues, while maintainers/admins see all.

**Endpoint**: `GET /api/issues/`

**Headers**:
```
Authorization: Token your_auth_token
```

**Response**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Bug in login page",
    "status": "OPEN",
    "severity": "HIGH",
    "created_at": "2023-07-04T12:00:00Z"
  }
]
```

### Get Issue
Get details of a specific issue.

**Endpoint**: `GET /api/issues/<issue_id>/`

**Headers**:
```
Authorization: Token your_auth_token
```

**Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Bug in login page",
  "description": "The login button doesn't work on mobile",
  "status": "OPEN",
  "severity": "HIGH",
  "created_by": 2,
  "created_at": "2023-07-04T12:00:00Z",
  "updated_at": "2023-07-04T12:00:00Z"
}
```

### Update Issue Status/Severity
Update the status and/or severity of an issue. Only available to admins and maintainers.

**Endpoint**: `PATCH /api/issues/<issue_id>/update-status/`

**Headers**:
```
Authorization: Token your_auth_token
Content-Type: application/json
```

**Request Body**:
```json
{
  "status": "IN_PROGRESS",
  "severity": "HIGH"
}
```

**Response**:
```json
{
  "message": "Issue updated successfully",
  "issue": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Bug in login page",
    "status": "IN_PROGRESS",
    "severity": "HIGH",
    "created_at": "2023-07-04T12:00:00Z",
    "updated_at": "2023-07-04T12:05:00Z"
  }
}
```

### Delete Issue
Delete an issue. Only available to maintainers and admins.

**Endpoint**: `DELETE /api/issues/<issue_id>/`

**Headers**:
```
Authorization: Token your_auth_token
```

**Response**:
```
HTTP 204 No Content
```

## Project Structure

The project follows a standard Django structure:

```
backend/
├── backend/            # Main project settings
│   ├── settings.py     # Project configuration
│   ├── urls.py         # Main URL routing
│   └── wsgi.py         # WSGI configuration
├── mainapp/            # Main application
│   ├── models.py       # Data models
│   ├── views.py        # API views
│   ├── urls.py         # API endpoints
│   ├── serializers.py  # Data serializers
│   ├── permissions.py  # Custom permissions
│   └── middleware.py   # Custom middleware
├── media/              # User-uploaded files
├── logs/               # Application logs
├── .env                # Environment variables
├── Dockerfile          # Docker configuration
├── manage.py           # Django management script
└── README.md           # Project documentation
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "error": "Not found."
}
```

## Issue Statistics

Get statistics about issues by status and severity.

**Endpoint**: `GET /api/issues/stats/`

**Headers**:
```
Authorization: Token your_auth_token
```

**Response**:
```json
{
  "status_counts": {
    "OPEN": 5,
    "TRIAGED": 2,
    "IN_PROGRESS": 3,
    "DONE": 1
  },
  "severity_counts": {
    "LOW": 1,
    "MEDIUM": 4,
    "HIGH": 5,
    "CRITICAL": 1
  },
  "total_issues": 11
}
```

## User Management

### User Roles

The system supports three user roles:

1. **Admin**: Full access to all features
2. **Maintainer**: Can triage and update issues
3. **Reporter**: Can create and view their own issues

### Get User Info

**Endpoint**: `GET /api/user/`

**Headers**:
```
Authorization: Token your_auth_token
```

**Response**:
```json
{
  "id": 1,
  "email": "admin@example.com",
  "name": "Admin User",
  "is_reporter": false,
  "is_maintainer": true,
  "is_admin": true
}
```

## Environment Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
   GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```

6. Set admin role (optional):
   ```bash
   python set_admin_role.py
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Docker Setup

You can also run the application using Docker:

```bash
# Build the Docker image
docker build -t deeplogic-backend .

# Run the container
docker run -p 8000:8000 -d --name deeplogic deeplogic-backend
```

## API Documentation

The API is documented using Swagger/OpenAPI. You can access the documentation at:

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`

## Testing

### Manual Testing

To test the API, you can use tools like [curl](https://curl.se/) or [Postman](https://www.postman.com/).

Example with curl:
```bash
# Get auth token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"yourpassword"}'

# Create an issue
curl -X POST http://localhost:8000/api/issues/create/ \
  -H "Authorization: Token your_auth_token" \
  -F "title=Test Issue" \
  -F "description=This is a test issue" \
  -F "severity=HIGH" \
  -F "attachment=@/path/to/file.txt"
```

### Automated Testing

The project includes automated tests:

```bash
# Run all tests
python manage.py test

# Run specific tests
python test_auth_api.py
python test_google_auth.py
```
