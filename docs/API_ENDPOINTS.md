# REST API Endpoints

This document provides an overview of all REST API endpoints implemented for the AI Mojo Assistant educational analytics system.

## Base URL
All endpoints are prefixed with `/api`

## Authentication
Currently, the API does not require authentication. This should be added in future versions.

## Users API

### Create User
- **Endpoint**: `POST /api/users/`
- **Description**: Create a new user
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"  // Enum: teacher, parent, student
  }
  ```
- **Response**: 201 Created

### List Users
- **Endpoint**: `GET /api/users/`
- **Description**: List users with pagination and optional role filtering
- **Query Parameters**:
  - `skip` (int, default=0): Number of records to skip
  - `limit` (int, default=100, max=100): Number of records to return
  - `role` (string, optional): Filter by role (teacher, parent, student)
- **Response**: 200 OK

### Get User
- **Endpoint**: `GET /api/users/{user_id}`
- **Description**: Get a specific user by ID
- **Response**: 200 OK or 404 Not Found

### Update User
- **Endpoint**: `PUT /api/users/{user_id}`
- **Description**: Update user information
- **Request Body**: Partial user object
- **Response**: 200 OK or 404 Not Found

### Delete User
- **Endpoint**: `DELETE /api/users/{user_id}`
- **Description**: Delete a user
- **Response**: 204 No Content or 404 Not Found

## Students API

### Create Student
- **Endpoint**: `POST /api/students/`
- **Description**: Create a new student profile
- **Request Body**:
  ```json
  {
    "user_id": 1,
    "class_name": "5A"
  }
  ```
- **Response**: 201 Created

### List Students
- **Endpoint**: `GET /api/students/`
- **Query Parameters**:
  - `skip` (int): Pagination offset
  - `limit` (int, max=100): Page size
  - `class_name` (string, optional): Filter by class
- **Response**: 200 OK

### Get/Update/Delete Student
- **Endpoints**: `GET/PUT/DELETE /api/students/{student_id}`
- **Similar to Users API**

## Teachers API

### Create Teacher
- **Endpoint**: `POST /api/teachers/`
- **Request Body**:
  ```json
  {
    "user_id": 2,
    "subjects": ["Mathematics", "Physics"]
  }
  ```
- **Response**: 201 Created

### List Teachers
- **Endpoint**: `GET /api/teachers/`
- **Query Parameters**: `skip`, `limit`
- **Response**: 200 OK

### Get/Update/Delete Teacher
- **Endpoints**: `GET/PUT/DELETE /api/teachers/{teacher_id}`

## Grades API

### Create Grade
- **Endpoint**: `POST /api/grades/`
- **Request Body**:
  ```json
  {
    "student_id": 1,
    "teacher_id": 1,
    "subject": "Mathematics",
    "grade": "5",
    "date": "2025-10-15T10:00:00",
    "lesson_topic": "Algebra"
  }
  ```
- **Response**: 201 Created

### List Grades
- **Endpoint**: `GET /api/grades/`
- **Query Parameters**:
  - `skip`, `limit`: Pagination
  - `student_id` (int, optional): Filter by student
  - `days` (int, optional): Only with student_id, get grades from last N days
- **Response**: 200 OK

### Get/Update/Delete Grade
- **Endpoints**: `GET/PUT/DELETE /api/grades/{grade_id}`

## Attendance API

### Mark Attendance
- **Endpoint**: `POST /api/attendance/`
- **Request Body**:
  ```json
  {
    "student_id": 1,
    "lesson_id": 1,
    "present": true,
    "date": "2025-10-15T10:00:00"
  }
  ```
- **Response**: 201 Created

### List/Get/Update/Delete Attendance
- **Endpoints**: `GET /api/attendance/`, `GET/PUT/DELETE /api/attendance/{attendance_id}`

## Homework API

### Create Homework
- **Endpoint**: `POST /api/homework/`
- **Request Body**:
  ```json
  {
    "title": "Math homework",
    "description": "Complete exercises 1-10",
    "due_date": "2025-10-20T23:59:59",
    "lesson_id": 1,
    "teacher_id": 2
  }
  ```
- **Response**: 201 Created

### List/Get/Update/Delete Homework
- **Endpoints**: `GET /api/homework/`, `GET/PUT/DELETE /api/homework/{homework_id}`

## Lessons API

### Create Lesson
- **Endpoint**: `POST /api/lessons/`
- **Request Body**:
  ```json
  {
    "subject": "Mathematics",
    "date": "2025-10-15T10:00:00",
    "topic": "Quadratic Equations",
    "class_name": "5A",
    "teacher_id": 2
  }
  ```
- **Response**: 201 Created

### List/Get/Update/Delete Lesson
- **Endpoints**: `GET /api/lessons/`, `GET/PUT/DELETE /api/lessons/{lesson_id}`

## Analytics API

### System Summary
- **Endpoint**: `GET /api/analytics/reports/summary`
- **Description**: Get overall system statistics
- **Response**:
  ```json
  {
    "summary": {
      "total_users": 10,
      "total_students": 5,
      "total_teachers": 3,
      "total_grades": 50,
      "total_lessons": 25
    },
    "timestamp": "2025-10-15T14:00:00"
  }
  ```

### Student Grades Summary
- **Endpoint**: `GET /api/analytics/student/{student_id}/grades-summary`
- **Query Parameters**:
  - `days` (int, default=30, max=365): Analysis period
- **Description**: Get grade summary and statistics for a specific student
- **Response**: Grade counts by subject and date range

### Class Overview
- **Endpoint**: `GET /api/analytics/class/{class_name}/overview`
- **Description**: Get overview of a specific class
- **Response**: Student count and recent activity

## Error Responses

All endpoints return standard HTTP status codes:
- `200 OK`: Successful GET/PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

Error responses include a detail field:
```json
{
  "detail": "Error message"
}
```

## OpenAPI Documentation

Interactive API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
