# Architecture

This document describes the architecture of the AI Mojo Assistant backend service.

## Overview

The service is built using FastAPI and integrates with Mojo.education API for educational data, using DeepSeek LLM for AI analysis.

## Components

- **API Layer**: FastAPI endpoints for health checks and analysis.
- **Services**: Scheduler for automated tasks, Analysis for grading checks and reports.
- **Integrations**: MojoClient for API communication.
- **Models**: SQLAlchemy models for database interactions.