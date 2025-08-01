# 🍳 Cookware Damage Analyzer

AI-powered cookware damage detection and safety analysis using TensorFlow. Analyze your cookware condition with computer vision and get actionable safety recommendations.

## 🚀 Live Demo

- **Koyeb**: [cookware-analyzer.koyeb.app](https://cookware-analyzer.koyeb.app)
- **Vercel**: [cookware-analyzer.vercel.app](https://cookware-analyzer.vercel.app)

## ✨ Features

- 📸 Upload cookware images for instant AI analysis
- 🤖 Advanced computer vision using optimized TensorFlow model
- 🏷️ Classify damage levels: New, Minor, Moderate, Severe
- 🔍 Detailed condition reports with safety recommendations
- 📊 Confidence scores and probability breakdowns
- 🎯 No API keys required - completely self-contained
- 🌐 Responsive web interface optimized for mobile

## 🏗️ Architecture

- **Frontend**: Vanilla HTML/CSS/JavaScript with responsive design
- **Backend**: Flask REST API with TensorFlow integration
- **Model**: Optimized cookware classifier (71.02% accuracy)
- **Deployment**: Multi-platform support (Koyeb + Vercel)

## � Quick Deployment

### Option 1: Automated Deployment Script

```bash
# Run the deployment script
python deploy.py

# Or directly specify platform
python deploy.py koyeb    # Deploy to Koyeb only
python deploy.py vercel   # Deploy to Vercel only
python deploy.py both     # Deploy to both platforms
```

### Option 2: Platform-Specific Commands

#### Deploy to Koyeb
```bash
# Install Koyeb CLI (if not installed)
curl -fsSL https://cli.koyeb.com/install.sh | sh

# Deploy
koyeb app deploy cookware-analyzer --config koyeb.yaml
```
