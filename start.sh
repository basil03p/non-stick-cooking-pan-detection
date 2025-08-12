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

# Check if wear multiclass model exists
if [ -f "models/wear_multiclass_model.h5" ]; then
    echo "✓ Wear multiclass model found"
else
    echo "⚠ Wear multiclass model not found, will try fallback models"
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
