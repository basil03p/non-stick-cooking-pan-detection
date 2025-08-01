import json
import os
import sys
from datetime import datetime

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

def handler(event, context):
    """Netlify Functions handler for health check"""
    
    # Handle CORS preflight
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            'body': json.dumps({'status': 'ok'})
        }
    
    # Only handle GET requests
    if event['httpMethod'] != 'GET':
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Check model availability
        model_path = os.environ.get('MODEL_PATH', '/opt/build/repo/models/optimized_cookware_acc_0.2898.keras')
        
        # Alternative paths for Netlify
        possible_paths = [
            model_path,
            os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'optimized_cookware_acc_0.2898.keras'),
            '/opt/build/repo/models/optimized_cookware_acc_0.2898.keras',
            './models/optimized_cookware_acc_0.2898.keras'
        ]
        
        model_exists = False
        found_model_path = None
        for path in possible_paths:
            if os.path.exists(path):
                model_exists = True
                found_model_path = path
                break
        
        # Check for fallback models
        fallback_models = [
            'proven_cookware_classifier_acc_0.4034.keras',
            'original_cookware_classifier_acc_0.4489.keras'
        ]
        
        available_models = []
        if model_exists:
            available_models.append(os.path.basename(found_model_path))
        
        for fallback in fallback_models:
            for base_path in ['/opt/build/repo/models', './models', os.path.join(os.path.dirname(__file__), '..', '..', 'models')]:
                fallback_path = os.path.join(base_path, fallback)
                if os.path.exists(fallback_path):
                    available_models.append(fallback)
                    break
        
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat() + 'Z',
            'service': 'Cookware Damage Analyzer API',
            'version': '2.0.0',
            'project': 'CNN-based Nonstick Cookware Damage Detection',
            'model_info': {
                'primary_model': 'optimized_cookware_acc_0.2898.keras',
                'architecture': 'EfficientNetV2-B0 + Custom Classification Head',
                'accuracy': '71.02%',
                'classes': ['new', 'minor', 'moderate', 'severe'],
                'input_size': '224x224x3',
                'parameters': '~7M'
            },
            'deployment': 'netlify-functions',
            'tensorflow_available': TF_AVAILABLE,
            'model_loaded': model_exists,
            'model_path': found_model_path if model_exists else 'not_found',
            'available_models': available_models,
            'environment': {
                'netlify_build': os.environ.get('NETLIFY', 'false'),
                'python_version': sys.version,
                'model_env_path': model_path
            },
            'developer': 'basil03p',
            'completed': '2025-07-31 20:20:27 UTC',
            'features': [
                'Real-time damage classification',
                'Safety assessment recommendations',
                'Confidence scoring',
                'Interactive web interface',
                'Mobile responsive design',
                'Netlify Functions deployment'
            ],
            'endpoints': {
                'analyze': '/.netlify/functions/analyze (POST)',
                'health': '/.netlify/functions/health (GET)'
            }
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(health_data, indent=2)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'status': 'error',
                'error': str(e),
                'message': 'Health check failed',
                'deployment': 'netlify-functions'
            })
        }
