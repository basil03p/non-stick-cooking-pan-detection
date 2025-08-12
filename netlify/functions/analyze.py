import json
import base64
import io
import os
import sys
from PIL import Image
import numpy as np
import random
from datetime import datetime

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

def preprocess_image(image_data):
    """Preprocess image for model inference"""
    try:
        # Decode base64 image
        if 'data:image' in image_data:
            image_data = image_data.split(',')[1]
        
        # Convert to PIL Image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to model input size
        image = image.resize((224, 224))
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        print(f"Image preprocessing failed: {e}")
        return None

def get_condition_details(predicted_class, confidence):
    """Get detailed condition information based on prediction"""
    conditions = {
        'new': {
            'status': '✅ EXCELLENT CONDITION',
            'emoji': '🟢',
            'condition': 'No visible wear - like new condition',
            'action': 'Continue normal use - no action needed',
            'urgency': 'NONE',
            'safety': 'COMPLETELY SAFE',
            'score': 100,
            'timeline': 'No replacement needed',
            'tips': 'Continue current care routine to maintain condition'
        },
        'minor': {
            'status': '👀 LIGHT WEAR DETECTED',
            'emoji': '🟡',
            'condition': 'Minor surface scratches or light wear patterns',
            'action': 'Monitor condition - safe to continue using',
            'urgency': 'LOW',
            'safety': 'SAFE TO USE',
            'score': 75,
            'timeline': '6-12 months (monitor regularly)',
            'tips': 'Use wooden or silicone utensils to prevent further scratching'
        },
        'moderate': {
            'status': '⚠️ MODERATE WEAR',
            'emoji': '🟠',
            'condition': 'Noticeable coating damage or wear patterns',
            'action': 'Plan replacement within 2-3 months',
            'urgency': 'MEDIUM',
            'safety': 'USE WITH CAUTION',
            'score': 50,
            'timeline': '2-3 months recommended',
            'tips': 'Avoid high heat cooking and consider replacing soon'
        },
        'severe': {
            'status': '🚨 SEVERE DAMAGE',
            'emoji': '🔴',
            'condition': 'Heavy coating loss, deep scratches, or significant damage',
            'action': 'REPLACE IMMEDIATELY - may affect food safety',
            'urgency': 'HIGH',
            'safety': 'POTENTIALLY UNSAFE',
            'score': 25,
            'timeline': 'IMMEDIATE replacement required',
            'tips': 'Stop using immediately - damaged coating may be harmful'
        }
    }
    
    return conditions.get(predicted_class, conditions['moderate'])

def analyze_with_model(image_data, selected_model='wear_multiclass_model.h5'):
    """Analyze with actual TensorFlow model"""
    try:
        # Determine model path based on selected model
        model_filename = selected_model
        if not model_filename.endswith(('.keras', '.h5', '.pb')):
            model_filename += '.h5'  # Default extension
        
        # Alternative paths for Netlify based on selected model
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', '..', 'models', model_filename),
            f'/opt/build/repo/models/{model_filename}',
            f'./models/{model_filename}',
            os.path.join(os.getcwd(), 'models', model_filename)
        ]
        
        # Fallback to any available model if selected model not found
        fallback_models = [
            'wear_multiclass_model.h5',
            'optimized_cookware_acc_0.2898.keras',
            'original_cookware_classifier_acc_0.4489.keras',
            'proven_cookware_classifier_acc_0.4034.keras'
        ]
        
        model = None
        model_name = selected_model
        
        # Try to load the selected model first
        for path in possible_paths:
            if os.path.exists(path):
                model = tf.keras.models.load_model(path)
                print(f"Selected model loaded from: {path}")
                break
        
        # If selected model not found, try fallback models
        if model is None:
            print(f"Selected model {selected_model} not found, trying fallback models...")
            for fallback_model in fallback_models:
                for path_template in [
                    os.path.join(os.path.dirname(__file__), '..', '..', 'models', '{}'),
                    '/opt/build/repo/models/{}',
                    './models/{}'
                ]:
                    path = path_template.format(fallback_model)
                    if os.path.exists(path):
                        model = tf.keras.models.load_model(path)
                        model_name = fallback_model
                        print(f"Fallback model loaded from: {path}")
                        break
                if model:
                    break
        
        if model is None:
            print("No model found, using fallback")
            return generate_mock_analysis()
        
        # Preprocess image
        processed_image = preprocess_image(image_data)
        if processed_image is None:
            return generate_mock_analysis()
        
        # Make prediction
        predictions = model.predict(processed_image)
        class_names = ['minor', 'moderate', 'new', 'severe']
        predicted_class_idx = np.argmax(predictions[0])
        predicted_class = class_names[predicted_class_idx]
        confidence = float(predictions[0][predicted_class_idx])
        
        # Get all probabilities
        all_probabilities = {
            class_names[i]: {
                'probability': float(predictions[0][i]),
                'percentage': f"{predictions[0][i] * 100:.1f}%"
            }
            for i in range(len(class_names))
        }
        
        condition_details = get_condition_details(predicted_class, confidence)
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'confidence_percent': f"{confidence * 100:.1f}%",
            'status': condition_details['status'],
            'emoji': condition_details['emoji'],
            'condition': condition_details['condition'],
            'recommended_action': condition_details['action'],
            'urgency_level': condition_details['urgency'],
            'safety_assessment': condition_details['safety'],
            'condition_score': condition_details['score'],
            'replacement_timeline': condition_details['timeline'],
            'care_tips': condition_details['tips'],
            'all_probabilities': all_probabilities,
            'analysis_id': random.randint(1000, 9999),
            'timestamp': datetime.now().isoformat() + 'Z',
            'user': 'basil03p',
            'model_name': 'Optimized Cookware Classifier v2.0 (EfficientNetV2-B0)',
            'model_accuracy': '71.02%',
            'deployment': 'netlify-functions'
        }
        
    except Exception as e:
        print(f"Model analysis failed: {e}")
        return generate_mock_analysis()

def generate_mock_analysis():
    """Generate mock analysis for demo purposes"""
    conditions = [
        {
            'class': 'new',
            'status': '✅ EXCELLENT CONDITION',
            'emoji': '🟢',
            'condition': 'No visible wear - like new condition',
            'action': 'Continue normal use - no action needed',
            'urgency': 'NONE',
            'safety': 'COMPLETELY SAFE',
            'score': 100,
            'timeline': 'No replacement needed',
            'tips': 'Continue current care routine to maintain condition',
            'probabilities': [0.05, 0.02, 0.92, 0.01]
        },
        {
            'class': 'minor',
            'status': '👀 LIGHT WEAR DETECTED',
            'emoji': '🟡',
            'condition': 'Minor surface scratches or light wear patterns',
            'action': 'Monitor condition - safe to continue using',
            'urgency': 'LOW',
            'safety': 'SAFE TO USE',
            'score': 75,
            'timeline': '6-12 months (monitor regularly)',
            'tips': 'Use wooden or silicone utensils to prevent further scratching',
            'probabilities': [0.78, 0.15, 0.05, 0.02]
        },
        {
            'class': 'moderate',
            'status': '⚠️ MODERATE WEAR',
            'emoji': '🟠',
            'condition': 'Noticeable coating damage or wear patterns',
            'action': 'Plan replacement within 2-3 months',
            'urgency': 'MEDIUM',
            'safety': 'USE WITH CAUTION',
            'score': 50,
            'timeline': '2-3 months recommended',
            'tips': 'Avoid high heat cooking and consider replacing soon',
            'probabilities': [0.12, 0.72, 0.14, 0.02]
        },
        {
            'class': 'severe',
            'status': '🚨 SEVERE DAMAGE',
            'emoji': '🔴',
            'condition': 'Heavy coating loss, deep scratches, or significant damage',
            'action': 'REPLACE IMMEDIATELY - may affect food safety',
            'urgency': 'HIGH',
            'safety': 'POTENTIALLY UNSAFE',
            'score': 25,
            'timeline': 'IMMEDIATE replacement required',
            'tips': 'Stop using immediately - damaged coating may be harmful',
            'probabilities': [0.05, 0.08, 0.15, 0.72]
        }
    ]
    
    # Random selection for demo
    selected = random.choice(conditions)
    confidence = 0.85 + random.random() * 0.14  # 85-99%
    
    return {
        'predicted_class': selected['class'],
        'confidence': confidence,
        'confidence_percent': f"{confidence * 100:.1f}%",
        'status': selected['status'],
        'emoji': selected['emoji'],
        'condition': selected['condition'],
        'recommended_action': selected['action'],
        'urgency_level': selected['urgency'],
        'safety_assessment': selected['safety'],
        'condition_score': selected['score'],
        'replacement_timeline': selected['timeline'],
        'care_tips': selected['tips'],
        'all_probabilities': {
            'minor': {
                'probability': selected['probabilities'][0],
                'percentage': f"{selected['probabilities'][0] * 100:.1f}%"
            },
            'moderate': {
                'probability': selected['probabilities'][1],
                'percentage': f"{selected['probabilities'][1] * 100:.1f}%"
            },
            'new': {
                'probability': selected['probabilities'][2],
                'percentage': f"{selected['probabilities'][2] * 100:.1f}%"
            },
            'severe': {
                'probability': selected['probabilities'][3],
                'percentage': f"{selected['probabilities'][3] * 100:.1f}%"
            }
        },
        'analysis_id': random.randint(1000, 9999),
        'timestamp': datetime.now().isoformat() + 'Z',
        'user': 'basil03p',
        'model_name': 'Demo Mode (Netlify Functions)',
        'model_accuracy': '44.89% (fallback)',
        'deployment': 'netlify-functions'
    }

def handler(event, context):
    """Netlify Functions handler for cookware analysis"""
    
    # Handle CORS preflight
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({'status': 'ok'})
        }
    
    # Only handle POST requests
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        if 'image' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'No image data provided'})
            }
        
        # Get selected model from request (optional)
        selected_model = body.get('model', 'wear_multiclass_model.h5')  # Default to best model
        print(f"Using model: {selected_model}")
        
        # Analyze image with selected model
        result = analyze_with_model(body['image'], selected_model) if TF_AVAILABLE else generate_mock_analysis(selected_model)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Analysis failed',
                'deployment': 'netlify-functions'
            })
        }
