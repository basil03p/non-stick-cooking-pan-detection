#!/bin/bash

# Koyeb startup script for Cookware Damage Analyzer
echo "Starting Cookware Damage Analyzer..."

# Set default port if not provided
export PORT=${PORT:-8080}

# Set TensorFlow environment variables
export TF_CPP_MIN_LOG_LEVEL=2
export PYTHONUNBUFFERED=1

# Check if models directory exists
if [ ! -d "models" ]; then
    echo "Warning: models directory not found"
fi

# Check if optimized model exists
if [ -f "models/optimized_cookware_acc_0.2898.keras" ]; then
    echo "✓ Optimized model found"
else
    echo "⚠ Optimized model not found, will try fallback models"
fi

# Start the application with gunicorn for better production performance
# Use gunicorn for production, fallback to python app.py for development
if [ "$FLASK_ENV" = "production" ]; then
    echo "Starting with gunicorn (production mode)"
    exec gunicorn --config gunicorn.conf.py app:app
else
    echo "Starting with Flask dev server"
    exec python app.py
fi
