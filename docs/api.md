# API Documentation

## Endpoints

- `GET /`: Root endpoint
- `GET /health`: Health check
- `POST /analyze-grades`: Trigger grade analysis

## Analytics Endpoints

### Student Analytics

- `POST /analytics/student/{student_id}/grades`: Analyze grade trends for a student
  - Query params: `days` (optional, default: 30) - Number of days to analyze
  - Returns: Grade trends across all subjects, average grade, and statistics

- `POST /analytics/student/{student_id}/attendance`: Analyze attendance patterns
  - Query params: `days` (optional, default: 30) - Number of days to analyze
  - Returns: Attendance statistics and AI-generated alerts if issues detected

- `POST /analytics/student/{student_id}/homework`: Analyze homework completion
  - Query params: `days` (optional, default: 30) - Number of days to analyze
  - Returns: Homework completion statistics and alerts for overdue assignments

- `POST /analytics/student/{student_id}/comprehensive`: Generate comprehensive report
  - Query params: `days` (optional, default: 30) - Number of days to analyze
  - Returns: Complete analysis including grades, attendance, homework, AI insights, and recommendations

## AI Features

The analytics service uses vLLM (DeepSeek) API to generate:

1. **Performance Insights**: AI-analyzed summaries of student performance
2. **Smart Alerts**: Contextual alerts for attendance, grades, and homework issues
3. **Personalized Recommendations**: Actionable recommendations for teachers and parents

## Automated Reports

The scheduler automatically runs the following tasks:

- **Every 10 minutes**: Check for missing grades and alert teachers
- **Every Monday at 9:00 AM**: Generate and send weekly performance reports to parents
- **Every day at 8:00 AM**: Check attendance patterns and send alerts if needed
- **Every day at 6:00 PM**: Check homework completion and send alerts for overdue assignments
