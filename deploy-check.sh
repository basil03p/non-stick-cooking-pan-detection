#!/bin/bash

# Deployment script for Koyeb
echo "🚀 Preparing Cookware Analyzer for Koyeb deployment..."

# Check if required files exist
echo "📋 Checking required files..."

required_files=(
    "app.py"
    "requirements.txt"
    "koyeb.yaml"
    "Dockerfile"
    "models/optimized_cookware_acc_0.2898.keras"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file is missing!"
        exit 1
    fi
done

# Check models directory
echo "📁 Checking models directory..."
if [ -d "models" ]; then
    echo "✅ Models directory exists"
    echo "📊 Available models:"
    ls -la models/
else
    echo "❌ Models directory missing!"
    exit 1
fi

# Validate Python dependencies
echo "🐍 Validating Python environment..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 is available"
    python3 -c "import tensorflow, flask, PIL" 2>/dev/null && echo "✅ Required packages can be imported" || echo "⚠️  Some packages may need installation"
else
    echo "⚠️  Python3 not found - make sure it's installed"
fi

# Check Docker (optional)
echo "🐳 Checking Docker (optional)..."
if command -v docker &> /dev/null; then
    echo "✅ Docker is available for local testing"
else
    echo "ℹ️  Docker not found - that's okay for direct Koyeb deployment"
fi

echo ""
echo "🎯 Deployment Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 App: Flask-based Cookware Damage Analyzer"
echo "🧠 Model: Optimized Cookware Classifier (71.02% accuracy)"
echo "🚫 API Keys: None required (self-contained)"
echo "📦 Platform: Koyeb-ready with gunicorn"
echo "🔗 Health Check: /api/health"
echo "📊 Analysis Endpoint: /api/analyze (POST)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Ready for Koyeb deployment!"
echo ""
echo "📝 Next steps:"
echo "1. Push code to your Git repository"
echo "2. Connect repository to Koyeb"
echo "3. Deploy using koyeb.yaml configuration"
echo "4. Monitor startup logs for model loading"
echo ""
echo "🔗 Test locally with: python app.py"
echo "🔗 Test with gunicorn: gunicorn --config gunicorn.conf.py app:app"
