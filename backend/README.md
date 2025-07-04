# DeepLogic Backend API

This is the backend API for the DeepLogic application, providing authentication and issue management functionality.

## Table of Contents
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

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Testing

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
