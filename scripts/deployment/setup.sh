#!/bin/bash
# Setup script for deployment

echo "Setting up AI Mojo Assistant..."

# Install dependencies
pip install -r requirements.txt

# Run migrations (if any)
# alembic upgrade head

echo "Setup complete."