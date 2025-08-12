import json
import os
import sys

def handler(event, context):
    """Netlify Functions handler for listing available models"""
    
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS request for CORS
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Get models directory path
        models_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
        
        # Alternative paths for different deployment environments
        possible_model_dirs = [
            models_dir,
            '/opt/build/repo/models',
            './models',
            os.path.join(os.getcwd(), 'models')
        ]
        
        models = []
        models_found = False
        
        for model_dir in possible_model_dirs:
            if os.path.exists(model_dir):
                models_found = True
                print(f"Found models directory: {model_dir}")
                
                # Scan for model files
                for filename in os.listdir(model_dir):
                    if filename.endswith(('.keras', '.h5', '.pb')):
                        file_path = os.path.join(model_dir, filename)
                        file_size = os.path.getsize(file_path)
                        
                        # Extract model information from filename
                        model_info = parse_model_filename(filename, file_size)
                        models.append(model_info)
                        
                break
        
        if not models_found:
            print("No models directory found")
            # Return default models for demo
            models = get_default_models()
        
        # Sort models by accuracy (descending)
        models.sort(key=lambda x: x['accuracy'], reverse=True)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'models': models,
                'total_count': len(models),
                'timestamp': '2025-08-12T00:00:00Z'
            })
        }
        
    except Exception as e:
        print(f"Error listing models: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Failed to load models',
                'message': str(e)
            })
        }

def parse_model_filename(filename, file_size):
    """Parse model filename to extract information"""
    
    # Convert bytes to MB
    size_mb = round(file_size / (1024 * 1024), 1)
    
    # Extract information from filename patterns
    model_info = {
        'filename': filename,
        'display_name': filename.replace('.keras', '').replace('.h5', '').replace('_', ' ').title(),
        'file_size': file_size,
        'size_mb': size_mb,
        'accuracy': 0.0,
        'model_type': 'unknown',
        'description': 'AI model for cookware analysis',
        'icon': '🤖',
        'badge': 'AI Model',
        'badge_type': 'default'
    }
    
    # Parse specific model types
    if 'wear_multiclass' in filename.lower():
        model_info.update({
            'display_name': 'Wear Multiclass Model',
            'accuracy': 72.5,
            'model_type': 'multiclass',
            'description': 'Advanced multiclass wear detection model',
            'icon': '🏆',
            'badge': 'High Performance',
            'badge_type': 'premium'
        })
    elif 'original' in filename.lower():
        accuracy = extract_accuracy_from_filename(filename)
        model_info.update({
            'display_name': 'Original Classifier',
            'accuracy': accuracy or 44.89,
            'model_type': 'baseline',
            'description': 'Original baseline classifier',
            'icon': '📊',
            'badge': 'Basic',
            'badge_type': 'info'
        })
    elif 'proven' in filename.lower():
        accuracy = extract_accuracy_from_filename(filename)
        model_info.update({
            'display_name': 'Proven Classifier',
            'accuracy': accuracy or 40.34,
            'model_type': 'research',
            'description': 'Proven research classifier',
            'icon': '🔬',
            'badge': 'Research',
            'badge_type': 'secondary'
        })
    
    return model_info

def extract_accuracy_from_filename(filename):
    """Extract accuracy percentage from filename"""
    import re
    
    # Look for patterns like "acc_0.4489" or "acc_0.2898"
    match = re.search(r'acc[_-]?(\d+\.\d+)', filename.lower())
    if match:
        return round(float(match.group(1)) * 100, 1)
    
    return None

def get_default_models():
    """Return default models for demo when no models directory is found"""
    return [
        {
            'filename': 'wear_multiclass_model.h5',
            'display_name': 'Wear Multiclass Model',
            'file_size': 178145280,
            'size_mb': 169.9,
            'accuracy': 72.5,
            'model_type': 'multiclass',
            'description': 'Advanced multiclass wear detection model',
            'icon': '🏆',
            'badge': 'High Performance',
            'badge_type': 'premium'
        },
        {
            'filename': 'original_cookware_classifier_acc_0.4489.keras',
            'display_name': 'Original Classifier',
            'file_size': 43429239,
            'size_mb': 41.4,
            'accuracy': 44.89,
            'model_type': 'baseline',
            'description': 'Original baseline classifier',
            'icon': '📊',
            'badge': 'Basic',
            'badge_type': 'info'
        },
        {
            'filename': 'proven_cookware_classifier_acc_0.4034.keras',
            'display_name': 'Proven Classifier',
            'file_size': 43429231,
            'size_mb': 41.4,
            'accuracy': 40.34,
            'model_type': 'research',
            'description': 'Proven research classifier',
            'icon': '🔬',
            'badge': 'Research',
            'badge_type': 'secondary'
        }
    ]
