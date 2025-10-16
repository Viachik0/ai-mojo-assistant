# AI Mojo Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Backend service for AI-powered educational analytics and automated messaging integrated with Mojo.education.

## Features

- 📊 **Comprehensive Analytics**
  - Grade trend analysis across all subjects
  - Attendance pattern monitoring
  - Homework completion tracking
  
- 🤖 **AI-Powered Insights**
  - OpenAI-powered performance insights
  - Intelligent alerts for concerning patterns
  - Personalized recommendations for teachers and parents
  
- 📈 **Automated Reporting**
  - Weekly performance reports for parents
  - Daily attendance and homework alerts
  - Teacher notifications for missing grades
  
- 🔔 **Smart Notifications**
  - Real-time alerts through Mojo.education
  - Context-aware messaging
  - Multi-channel communication
  
- ⏰ **Scheduled Tasks**
  - Automated grading timeliness monitoring
  - Periodic analytics and reporting
  - Configurable scheduling

## Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/ai-mojo-assistant
cd ai-mojo-assistant

# Setup environment
cp .env.example .env
# Edit .env with your Mojo API credentials

# Run with Docker
docker-compose up -d

# Or run locally
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:

- **Interactive API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Key Endpoints

#### Analytics Endpoints

- `POST /analytics/student/{student_id}/grades?days=30` - Analyze grade trends
- `POST /analytics/student/{student_id}/attendance?days=30` - Analyze attendance patterns
- `POST /analytics/student/{student_id}/homework?days=30` - Analyze homework completion
- `POST /analytics/student/{student_id}/comprehensive?days=30` - Generate comprehensive AI report

#### Admin Endpoints

- `POST /analyze-grades` - Trigger manual grade analysis

See [docs/api.md](docs/api.md) for complete API documentation.

## Configuration

Set these environment variables in your `.env` file:

**Mojo.education API:**
- `MOJO_API_KEY`: Your Mojo.education API key
- `MOJO_BASE_URL`: Mojo API base URL (default: https://mojo.education/api)

**AI Configuration:**
- `OPENAI_API_KEY`: Your OpenAI API key for AI-powered insights
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-3.5-turbo)
- `DEEPSEEK_API_URL`: DeepSeek LLM endpoint (optional alternative)

**Database:**
- `DATABASE_URL`: PostgreSQL connection string

**Application Settings:**
- `CHECK_INTERVAL_MINUTES`: Frequency of scheduled checks (default: 60)
- `GRADING_DEADLINE_DAYS`: Days before grading deadline (default: 3)
- `WEEKLY_REPORT_DAY`: Day for weekly reports (default: monday)

**Security:**
- `JWT_SECRET_KEY`: Secret key for JWT authentication

## Development

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Start development server
uvicorn app.main:app --reload
```

## License

MIT License - see LICENSE file for details.