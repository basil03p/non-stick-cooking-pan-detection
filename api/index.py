# Vercel serverless entry point
import os
import sys
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main Flask app
from app import app, load_model

# Configure for serverless environment
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model on cold start (Vercel will cache this)
try:
    model_loaded = load_model()
    if model_loaded:
        logger.info("Model loaded successfully for Vercel deployment")
    else:
        logger.warning("Model failed to load - using fallback analysis")
except Exception as e:
    logger.error(f"Error loading model in Vercel: {str(e)}")

# Vercel expects a handler function
def handler(request, response):
    return app(request, response)

# Export the app for Vercel
if __name__ == "__main__":
    app.run()
else:
    # For Vercel serverless
    application = app
