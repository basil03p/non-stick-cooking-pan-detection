import os
import json
import re
from pathlib import Path
from datetime import datetime

def handler(event, context):
    """
    Serverless function to dynamically detect available models
    """
    try:
        # Handle CORS preflight
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Get the models directory path - try multiple locations
        possible_paths = [
            Path(__file__).parent.parent / 'models',
            Path('/opt/build/repo/models'),  # Netlify build path
            Path('./models'),
            Path('../models')
        ]
        
        models_dir = None
        for path in possible_paths:
            if path.exists():
                models_dir = path
                break
        
        if not models_dir:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({
                    'status': 'error',
                    'message': 'Models directory not found',
                    'models': [],
                    'searched_paths': [str(p) for p in possible_paths]
                })
            }
        
        models = []
        
        # Scan for model files
        model_extensions = ['*.keras', '*.h5', '*.pb', '*.pkl', '*.joblib']
        for pattern in model_extensions:
            for model_file in models_dir.glob(pattern):
                model_info = parse_model_filename(model_file.name, model_file)
                if model_info:
                    models.append(model_info)
        
        # Sort by accuracy (highest first)
        models.sort(key=lambda x: x['accuracy'], reverse=True)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'success',
                'models': models,
                'count': len(models),
                'timestamp': datetime.now().isoformat(),
                'models_dir': str(models_dir)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'status': 'error',
                'message': f'Failed to scan models: {str(e)}',
                'models': [],
                'timestamp': datetime.now().isoformat()
            })
        }

def parse_model_filename(filename, file_path=None):
    """Parse model filename to extract information"""
    try:
        # Remove file extension
        base_name = filename
        for ext in ['.keras', '.h5', '.pb', '.pkl', '.joblib']:
            base_name = base_name.replace(ext, '')
        
        # Extract accuracy using regex patterns
        accuracy_patterns = [
            r'acc[_-]?(\d+\.?\d*)',  # acc_0.2898 or acc-0.2898
            r'accuracy[_-]?(\d+\.?\d*)',  # accuracy_0.2898
            r'(\d+\.\d+)[_-]?acc',  # 0.2898_acc
            r'[_-](\d+\.\d+)$',  # ending with _0.2898
        ]
        
        accuracy = 0.0
        for pattern in accuracy_patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                acc_val = float(match.group(1))
                # Convert to percentage if it's a decimal
                if acc_val <= 1.0:
                    accuracy = acc_val * 100
                else:
                    accuracy = acc_val
                break
        
        # Get file stats if available
        file_size = 0
        modified_date = None
        if file_path and file_path.exists():
            try:
                stat = file_path.stat()
                file_size = round(stat.st_size / (1024 * 1024), 2)  # MB
                modified_date = datetime.fromtimestamp(stat.st_mtime).isoformat()
            except:
                pass
        
        # Generate model metadata
        model_type = generate_model_type(base_name)
        display_name = generate_display_name(base_name)
        model_category = determine_model_category(base_name, accuracy)
        
        return {
            'id': model_type,
            'filename': filename,
            'name': display_name,
            'accuracy': round(accuracy, 2),
            'accuracy_display': f"{accuracy:.1f}%",
            'category': model_category['category'],
            'badge': model_category['badge'],
            'color': model_category['color'],
            'icon': model_category['icon'],
            'description': model_category['description'],
            'file_size_mb': file_size,
            'modified_date': modified_date,
            'recommended': accuracy >= 60,
            'type': determine_model_type_from_name(base_name)
        }
        
    except Exception as e:
        print(f"Error parsing filename {filename}: {e}")
        return None

def generate_model_type(base_name):
    """Generate a clean model type identifier"""
    # Remove common suffixes and prefixes
    clean_name = base_name.lower()
    clean_name = re.sub(r'(_acc[_-]?\d+\.?\d*|_accuracy[_-]?\d+\.?\d*|_classifier|_model)', '', clean_name)
    clean_name = re.sub(r'(cookware[_-]?|damage[_-]?|detection[_-]?)', '', clean_name)
    clean_name = clean_name.strip('_-')
    
    # If empty, use the original base name
    if not clean_name:
        clean_name = base_name.lower()
    
    return clean_name.replace('_', '-')

def generate_display_name(base_name):
    """Generate a human-readable display name"""
    # Remove accuracy and common suffixes
    clean_name = re.sub(r'(_acc[_-]?\d+\.?\d*|_accuracy[_-]?\d+\.?\d*)', '', base_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'(_classifier|_model)', '', clean_name, flags=re.IGNORECASE)
    
    # Split on underscores/hyphens and capitalize
    words = re.split(r'[_-]', clean_name)
    words = [word.capitalize() for word in words if word]
    
    return ' '.join(words)

def determine_model_category(base_name, accuracy):
    """Determine model category based on accuracy and name"""
    name_lower = base_name.lower()
    
    if accuracy >= 70:
        return {
            'category': 'premium',
            'badge': '⚡ Excellent',
            'color': 'green',
            'icon': '🏆',
            'description': f'High-performance model with {accuracy:.1f}% accuracy'
        }
    elif accuracy >= 60:
        return {
            'category': 'standard',
            'badge': '🎯 Good',
            'color': 'blue', 
            'icon': '🎯',
            'description': f'Reliable model with {accuracy:.1f}% accuracy'
        }
    elif accuracy >= 45:
        return {
            'category': 'basic',
            'badge': '📊 Fair',
            'color': 'orange',
            'icon': '📊',
            'description': f'Basic model with {accuracy:.1f}% accuracy'
        }
    else:
        return {
            'category': 'experimental',
            'badge': '🧪 Experimental',
            'color': 'purple',
            'icon': '🧪',
            'description': f'Experimental model with {accuracy:.1f}% accuracy'
        }

def determine_model_type_from_name(base_name):
    """Determine specific model type from filename"""
    name_lower = base_name.lower()
    
    if 'optimized' in name_lower or 'enhanced' in name_lower:
        return 'optimized'
    elif 'proven' in name_lower or 'stable' in name_lower:
        return 'proven'
    elif 'original' in name_lower or 'base' in name_lower:
        return 'original'
    elif 'wear' in name_lower and 'multiclass' in name_lower:
        return 'wear_multiclass'
    elif 'experimental' in name_lower or 'test' in name_lower:
        return 'experimental'
    else:
        return 'custom'
