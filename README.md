# AI Mojo Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Backend service for AI-powered educational analytics and automated messaging integrated with Mojo.education.

## Features

- 📊 Automated grading timeliness monitoring
- 📈 Weekly performance reports for parents
- 🤖 AI-powered analysis using DeepSeek LLM
- 🔔 Smart notifications through Mojo.education
- ⏰ Scheduled tasks and analytics

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

API Docs: http://localhost:8000/docs
Health Check: http://localhost:8000/health

## Configuration

Set these environment variables:

MOJO_API_KEY: Your Mojo.education API key
MOJO_BASE_URL: Mojo API base URL
DEEPSEEK_API_URL: DeepSeek LLM endpoint
DATABASE_URL: PostgreSQL connection string

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