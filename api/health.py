from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Check model availability
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'optimized_cookware_acc_0.2898.keras')
        model_exists = os.path.exists(model_path)
        
        # Check for fallback models
        fallback_models = [
            'proven_cookware_classifier_acc_0.4034.keras',
            'original_cookware_classifier_acc_0.4489.keras'
        ]
        
        available_models = []
        if model_exists:
            available_models.append('optimized_cookware_acc_0.2898.keras')
        
        for fallback in fallback_models:
            fallback_path = os.path.join(os.path.dirname(__file__), '..', 'models', fallback)
            if os.path.exists(fallback_path):
                available_models.append(fallback)
        
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
            'tensorflow_available': TF_AVAILABLE,
            'model_loaded': model_exists,
            'available_models': available_models,
            'deployment': 'vercel-serverless',
            'developer': 'basil03p',
            'completed': '2025-07-31 20:20:27 UTC',
            'features': [
                'Real-time damage classification',
                'Safety assessment recommendations', 
                'Confidence scoring',
                'Interactive web interface',
                'Mobile responsive design'
            ],
            'endpoints': {
                'analyze': '/api/analyze (POST)',
                'health': '/api/health (GET)'
            }
        }
        
        response = json.dumps(health_data, indent=2)
        self.wfile.write(response.encode())