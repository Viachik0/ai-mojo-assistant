# Quick Reference Guide - Analytics Service

## API Endpoints

### 1. Analyze Student Grades
Analyzes grade trends across all subjects for a specific student.

**Endpoint:** `POST /analytics/student/{student_id}/grades`

**Parameters:**
- `student_id` (path): Student ID
- `days` (query, optional): Number of days to analyze (default: 30, max: 365)

**Example:**
```bash
curl -X POST "http://localhost:8000/analytics/student/1/grades?days=30"
```

**Response:**
```json
{
  "student_id": 1,
  "status": "success",
  "average_grade": 4.5,
  "grade_trends": {
    "Math": {
      "subject": "Math",
      "average": 4.75,
      "trend": "stable",
      "count": 10,
      "latest_grade": 5.0,
      "highest_grade": 5.0,
      "lowest_grade": 4.0
    }
  },
  "total_grades": 25,
  "subjects_count": 3
}
```

### 2. Analyze Student Attendance
Analyzes attendance patterns and generates alerts if issues are detected.

**Endpoint:** `POST /analytics/student/{student_id}/attendance`

**Parameters:**
- `student_id` (path): Student ID
- `days` (query, optional): Number of days to analyze (default: 30)

**Example:**
```bash
curl -X POST "http://localhost:8000/analytics/student/1/attendance?days=7"
```

**Response:**
```json
{
  "student_id": 1,
  "status": "success",
  "attendance_stats": {
    "total_lessons": 10,
    "present_count": 9,
    "absent_count": 1,
    "attendance_rate": 90.0
  },
  "alerts": []
}
```

### 3. Analyze Homework Completion
Tracks homework completion rates and identifies overdue assignments.

**Endpoint:** `POST /analytics/student/{student_id}/homework`

**Parameters:**
- `student_id` (path): Student ID
- `days` (query, optional): Number of days to analyze (default: 30)

**Example:**
```bash
curl -X POST "http://localhost:8000/analytics/student/1/homework?days=14"
```

**Response:**
```json
{
  "student_id": 1,
  "status": "success",
  "homework_stats": {
    "total_assignments": 10,
    "completed_count": 8,
    "completion_rate": 80.0,
    "overdue_count": 2
  },
  "alerts": ["You have 2 overdue assignments. Please complete them soon."]
}
```

### 4. Generate Comprehensive Report
Generates a complete analytics report with AI-powered insights and recommendations.

**Endpoint:** `POST /analytics/student/{student_id}/comprehensive`

**Parameters:**
- `student_id` (path): Student ID
- `days` (query, optional): Number of days to analyze (default: 30)

**Example:**
```bash
curl -X POST "http://localhost:8000/analytics/student/1/comprehensive?days=30"
```

**Response:**
```json
{
  "student_id": 1,
  "status": "success",
  "period_days": 30,
  "grades": { /* grade analysis */ },
  "attendance": { /* attendance analysis */ },
  "homework": { /* homework analysis */ },
  "ai_insights": "The student shows strong performance in Mathematics with a stable trend. Attendance is excellent at 95%. Consider focusing more attention on completing homework on time to maintain this positive trajectory.",
  "recommendations": "1. Continue current study habits in Mathematics\n2. Set reminders for homework deadlines\n3. Maintain excellent attendance record"
}
```

## Automated Tasks

The scheduler automatically runs the following analytics tasks:

| Task | Schedule | Description |
|------|----------|-------------|
| Check Missing Grades | Every 10 minutes | Alerts teachers about lessons without grades |
| Weekly Reports | Monday 9:00 AM | Sends AI-powered performance reports to parents |
| Attendance Alerts | Daily 8:00 AM | Checks attendance patterns and sends alerts |
| Homework Alerts | Daily 6:00 PM | Checks for overdue homework and sends notifications |

## Python Usage Examples

### Using the Analytics Service Directly

```python
from app.services.analysis_service import AnalysisService
from app.integrations.mojo_client import MojoClient

# Initialize
mojo_client = MojoClient(base_url, api_key)
analytics = AnalysisService(mojo_client)

# Analyze grades
grades = await analytics.analyze_student_grades(student_id=1, days=30)

# Generate comprehensive report
report = await analytics.generate_comprehensive_report(student_id=1, days=30)
print(report['ai_insights'])
print(report['recommendations'])
```

### Using the Database Service

```python
from app.services.database_service import DatabaseService

db_service = DatabaseService()

# Get grade trends
trends = await db_service.get_grade_trends(
    student_id=1, 
    subject="Mathematics", 
    days=30
)

# Get attendance stats
stats = await db_service.get_attendance_stats(student_id=1, days=7)

# Get homework completion rate
homework = await db_service.get_homework_completion_rate(student_id=1, days=14)
```

## Configuration

Add these environment variables to your `.env` file:

```bash
# OpenAI Configuration (Required for AI insights)
OPENAI_API_KEY=sk-...your-key-here...
OPENAI_MODEL=gpt-3.5-turbo

# Mojo.education API
MOJO_API_KEY=your_mojo_api_key
MOJO_BASE_URL=https://mojo.education/api

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db

# Optional Settings
CHECK_INTERVAL_MINUTES=60
GRADING_DEADLINE_DAYS=3
WEEKLY_REPORT_DAY=monday
```

## Trend Analysis Interpretation

### Grade Trends
- **improving**: Second half average is 0.5+ points higher than first half
- **declining**: Second half average is 0.5+ points lower than first half
- **stable**: Difference is less than 0.5 points
- **insufficient_data**: Not enough grades to determine trend

### Attendance Alerts
- Triggered when attendance rate < 75%
- AI generates contextual alert message

### Homework Alerts
- Triggered when overdue count > 2
- AI generates actionable recommendations

## Error Handling

All endpoints return standard error responses:

```json
{
  "detail": "Error message here"
}
```

HTTP Status Codes:
- `200`: Success
- `500`: Internal server error

## Next Steps

1. Configure OpenAI API key for AI-powered insights
2. Test endpoints using the examples above
3. Monitor scheduled tasks in logs
4. Customize alert thresholds in the code if needed
5. Integrate with your frontend application

For more details, see:
- [API Documentation](api.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)
- [README](../README.md)
