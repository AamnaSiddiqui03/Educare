# NGO Mentorship Platform - API Documentation

## Overview
This document provides comprehensive API documentation for the NGO Mentorship Platform backend. All endpoints are RESTful and return JSON responses.

**Base URL:** `http://localhost:8000/api/v1`

---

## 🔐 Authentication

### Register User
**POST** `/auth/register`

Register a new user in the system.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "role": "student"  // "student", "donor", or "mentor"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student",
  "verified": false,
  "created_at": "2025-01-04T12:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request` - Email already registered
- `422 Unprocessable Entity` - Validation errors

---

### Login User
**POST** `/auth/login`

Authenticate user and get access token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "uuid-string",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials

---

### Logout User
**POST** `/auth/logout`

Logout the current user.

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

---

## 👥 User Management

### Get All Users
**GET** `/users/`

Get a list of all users in the system. **No authentication required.**

**Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student",
    "verified": false,
    "created_at": "2025-01-04T12:00:00Z"
  },
  {
    "id": "uuid-string-2",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "role": "mentor",
    "verified": true,
    "created_at": "2025-01-04T11:00:00Z"
  }
]
```

---

### Get Current User
**GET** `/users/me`

Get current authenticated user's details.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student",
  "verified": false,
  "created_at": "2025-01-04T12:00:00Z"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
- `404 Not Found` - User not found

---

### Get User by ID
**GET** `/users/{user_id}`

Get user details by user ID. Users can only access their own data.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Parameters:**
- `user_id` (string) - UUID of the user

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student",
  "verified": false,
  "created_at": "2025-01-04T12:00:00Z"
}
```

**Error Responses:**
- `403 Forbidden` - Trying to access another user's data
- `404 Not Found` - User not found

---

## 🎓 Student Profile Management

### Create Student Profile
**POST** `/students/{user_id}/profile`

Create a student profile for the authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "phone": "1234567890",
  "address": "123 Main Street, City, State 12345",
  "photo_url": "https://example.com/photo.jpg",  // Optional
  "video_url": "https://example.com/video.mp4",  // Optional
  "help_text": "I need help with career guidance and academic support."
}
```

**Response (201 Created):**
```json
{
  "student_id": "uuid-string",
  "user_id": "uuid-string",
  "phone": "1234567890",
  "address": "123 Main Street, City, State 12345",
  "photo_url": "https://example.com/photo.jpg",
  "video_url": "https://example.com/video.mp4",
  "help_text": "I need help with career guidance and academic support.",
  "profile_completed": false,
  "assessment_completed": false,
  "created_at": "2025-01-04T12:00:00Z",
  "updated_at": "2025-01-04T12:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request` - Profile already exists
- `403 Forbidden` - Not authorized to create profile for this user

---

### Get Student Profile
**GET** `/students/{user_id}/profile`

Get the student profile for the authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "student_id": "uuid-string",
  "user_id": "uuid-string",
  "phone": "1234567890",
  "address": "123 Main Street, City, State 12345",
  "photo_url": "https://example.com/photo.jpg",
  "video_url": "https://example.com/video.mp4",
  "help_text": "I need help with career guidance and academic support.",
  "profile_completed": false,
  "assessment_completed": false,
  "created_at": "2025-01-04T12:00:00Z",
  "updated_at": "2025-01-04T12:00:00Z"
}
```

**Error Responses:**
- `404 Not Found` - Profile not found

---

### Update Student Profile
**PUT** `/students/{user_id}/profile`

Update the student profile. All fields are optional.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "phone": "9876543210",  // Optional
  "address": "456 New Street, City, State 54321",  // Optional
  "help_text": "Updated help text."  // Optional
}
```

**Response (200 OK):**
```json
{
  "student_id": "uuid-string",
  "user_id": "uuid-string",
  "phone": "9876543210",
  "address": "456 New Street, City, State 54321",
  "photo_url": "https://example.com/photo.jpg",
  "video_url": "https://example.com/video.mp4",
  "help_text": "Updated help text.",
  "profile_completed": false,
  "assessment_completed": false,
  "created_at": "2025-01-04T12:00:00Z",
  "updated_at": "2025-01-04T12:30:00Z"
}
```

---

### Submit Student Profile
**POST** `/students/{user_id}/profile/submit`

Mark the student profile as completed.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "profile_completed": true,
  "message": "Profile completed successfully"
}
```

---

### Get Student Progress
**GET** `/students/{user_id}/profile/progress`

Get the student's progress status.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "profile_completed": true,
  "assessment_completed": false,
  "message": "Profile completed. Assessment pending."
}
```

---

## 📚 Education Management

### Add Education Entry
**POST** `/students/{user_id}/education`

Add an education entry for the student.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "institution_name": "University of Technology",
  "education_level": "Undergraduate",
  "year_of_passing": "2023",
  "marks_obtained": "85.5",
  "report_card_url": "https://example.com/report.pdf"  // Optional
}
```

**Response (201 Created):**
```json
{
  "education_id": "uuid-string",
  "student_id": "uuid-string",
  "institution_name": "University of Technology",
  "education_level": "Undergraduate",
  "year_of_passing": "2023",
  "marks_obtained": "85.5",
  "report_card_url": "https://example.com/report.pdf",
  "created_at": "2025-01-04T12:00:00Z",
  "updated_at": "2025-01-04T12:00:00Z"
}
```

---

### Get Education Entries
**GET** `/students/{user_id}/education`

Get all education entries for the student.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "education_id": "uuid-string",
    "student_id": "uuid-string",
    "institution_name": "University of Technology",
    "education_level": "Undergraduate",
    "year_of_passing": "2023",
    "marks_obtained": "85.5",
    "report_card_url": "https://example.com/report.pdf",
    "created_at": "2025-01-04T12:00:00Z",
    "updated_at": "2025-01-04T12:00:00Z"
  }
]
```

---

### Get Education Entry by ID
**GET** `/students/{user_id}/education/{education_id}`

Get a specific education entry.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "education_id": "uuid-string",
  "student_id": "uuid-string",
  "institution_name": "University of Technology",
  "education_level": "Undergraduate",
  "year_of_passing": "2023",
  "marks_obtained": "85.5",
  "report_card_url": "https://example.com/report.pdf",
  "created_at": "2025-01-04T12:00:00Z",
  "updated_at": "2025-01-04T12:00:00Z"
}
```

---

### Update Education Entry
**PUT** `/students/{user_id}/education/{education_id}`

Update an education entry. All fields are optional.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "marks_obtained": "90.0",  // Optional
  "report_card_url": "https://example.com/updated-report.pdf"  // Optional
}
```

**Response (200 OK):**
```json
{
  "education_id": "uuid-string",
  "student_id": "uuid-string",
  "institution_name": "University of Technology",
  "education_level": "Undergraduate",
  "year_of_passing": "2023",
  "marks_obtained": "90.0",
  "report_card_url": "https://example.com/updated-report.pdf",
  "created_at": "2025-01-04T12:00:00Z",
  "updated_at": "2025-01-04T12:30:00Z"
}
```

---

### Delete Education Entry
**DELETE** `/students/{user_id}/education/{education_id}`

Delete an education entry.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Education entry deleted successfully"
}
```

---

## 📝 Assessment System

### Get Available Assessments
**GET** `/students/{user_id}/assessment/available`

Get list of available assessments for the student.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "assessment_id": "uuid-string",
    "assessment_name": "Career Guidance Test",
    "assessment_type": "aptitude",
    "description": "A comprehensive career guidance assessment",
    "total_questions": "10",
    "time_limit_minutes": "30"
  }
]
```

---

### Start Assessment
**GET** `/students/{user_id}/assessment/start/{assessment_id}`

Start an assessment and get questions.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "assessment_id": "uuid-string",
  "assessment_name": "Career Guidance Test",
  "assessment_type": "aptitude",
  "description": "A comprehensive career guidance assessment",
  "total_questions": "10",
  "time_limit_minutes": "30",
  "questions": {
    "q1": {
      "question_id": "q1",
      "question_text": "What field interests you most?",
      "options": ["Technology", "Science", "Arts", "Business"]
    },
    "q2": {
      "question_id": "q2",
      "question_text": "How do you prefer to learn?",
      "options": ["Visual", "Auditory", "Reading", "Hands-on"]
    }
  },
  "message": "Assessment started successfully"
}
```

---

### Submit Assessment
**POST** `/students/{user_id}/assessment/submit/{assessment_id}`

Submit assessment answers.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "answers": {
    "q1": "Technology",
    "q2": "Visual",
    "q3": "Career Advancement"
  }
}
```

**Response (201 Created):**
```json
{
  "submission_id": "uuid-string",
  "assessment_id": "uuid-string",
  "assessment_name": "Career Guidance Test",
  "assessment_completed": true,
  "report_pdf_url": "https://example.com/report.pdf",
  "submitted_at": "2025-01-04T12:00:00Z",
  "message": "Assessment completed successfully"
}
```

---

### Get Assessment Report
**GET** `/students/{user_id}/assessment/report/{submission_id}`

Get assessment report and PDF download link.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "submission_id": "uuid-string",
  "student_id": "uuid-string",
  "assessment_id": "uuid-string",
  "assessment_name": "Career Guidance Test",
  "report_pdf_url": "https://example.com/report.pdf",
  "submitted_at": "2025-01-04T12:00:00Z"
}
```

---

### Get Assessment History
**GET** `/students/{user_id}/assessment/history`

Get all assessment submissions for the student.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "submission_id": "uuid-string",
    "assessment_id": "uuid-string",
    "assessment_name": "Career Guidance Test",
    "assessment_type": "aptitude",
    "report_pdf_url": "https://example.com/report.pdf",
    "submitted_at": "2025-01-04T12:00:00Z"
  }
]
```

---

## 🔧 Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "detail": "Error message describing the issue"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Invalid or missing authentication token"
}
```

**403 Forbidden:**
```json
{
  "detail": "You don't have permission to access this resource"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**422 Unprocessable Entity:**
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "An internal server error occurred"
}
```

---

## 🔑 Authentication

### JWT Token Usage
All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Token Expiration
- Tokens expire after 30 minutes by default
- Refresh tokens are not implemented yet
- Re-login required after token expiration

---

## 📝 Notes for Frontend Development

1. **User Roles**: The system supports three roles: `student`, `donor`, and `mentor`
2. **UUIDs**: All IDs are UUID strings
3. **Timestamps**: All timestamps are in ISO 8601 format
4. **File URLs**: Photo, video, and report URLs should be stored as full URLs
5. **Assessment Questions**: Questions come from external sources (placeholder implementation)
6. **PDF Reports**: Assessment reports are generated as PDFs (placeholder implementation)
7. **Validation**: Student-related validations have been removed for easier testing

---

## 🚀 Getting Started

1. **Register** a user with `/auth/register`
2. **Login** with `/auth/login` to get JWT token
3. **Create student profile** with `/students/{user_id}/profile`
4. **Add education entries** with `/students/{user_id}/education`
5. **Take assessments** with `/students/{user_id}/assessment/start/{assessment_id}`

For any questions or issues, please contact the backend development team.
