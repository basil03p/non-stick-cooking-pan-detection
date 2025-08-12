# 🍳 Cookware Damage Analyzer

**AI-powered cookware condition assessment using deep learning**

This project uses a CNN (EfficientNetV2-B0) to analyze images of cookware and classify their condition. The wear multiclass model achieves 72.5% accuracy with no external API dependencies.

## 🌐 Multi-Platform Deployment

Deploy on **3 different platforms** with a single codebase:

### 🚀 Quick Deploy

| Platform | Type | Deploy |
|----------|------|--------|
| **Koyeb** | Container/Server | [Deploy to Koyeb](https://app.koyeb.com/deploy) |
| **Vercel** | Serverless | [Deploy to Vercel](https://vercel.com/new) |
| **Netlify** | JAMstack + Functions | [Deploy to Netlify](https://app.netlify.com/start) |

---

## � Features

- **No API Keys Required** - Self-contained ML model
- **Fast Analysis** - EfficientNetV2-B0 optimized for speed
- **72.5% Accuracy** - Proven model performance
- **Multi-Platform** - Deploy anywhere
- **Responsive UI** - Works on all devices

---

## 🔧 Local Development

### Prerequisites
- Python 3.11+
- Node.js (for Vercel CLI)
- Docker (optional)

### Setup
```bash
# Clone repository
git clone <your-repo>
cd cookware-analyzer

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

Visit `http://localhost:5000`

---

## 🏗️ Deployment Guides

### 1. 🚀 Koyeb (Recommended for Production)

**Best for: Production workloads, consistent traffic**

```bash
# 1. Connect your repository to Koyeb
# 2. Use these settings:
Build Command: pip install -r requirements.txt
Run Command: gunicorn app:app --bind 0.0.0.0:$PORT
```

**Configuration file:** `koyeb.yaml`
- Uses Gunicorn WSGI server
- Optimized for TensorFlow workloads
- Automatic SSL and scaling

### 2. ⚡ Vercel (Serverless)

**Best for: Variable traffic, cost optimization**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Configuration file:** `vercel.json`
- Serverless functions in `/api`
- Automatic edge caching
- Global CDN distribution

### 3. 🌐 Netlify (JAMstack + Functions)

**Best for: Static sites with API functionality**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build and deploy
netlify build
netlify deploy --prod
```

**Build Commands:**
```bash
Build command: pip install -r requirements.txt
Publish directory: public
Functions directory: netlify/functions
```

**Configuration file:** `netlify.toml`
- Static site serving from `/public`
- Serverless functions for ML analysis
- Built-in form handling

---

## � Project Structure

```
cookware-analyzer/
├── 📱 Frontend
│   └── public/
│       ├── index.html          # Main interface
│       ├── script.js           # Upload logic
│       └── styles.css          # Responsive design
│
├── 🤖 ML Model
│   └── models/
│       └── wear_multiclass_model.h5  # 72.5% accuracy
│
├── 🔧 Backend APIs
│   ├── app.py                  # Main Flask app (Koyeb)
│   ├── api/                    # Vercel functions
│   │   ├── analyze.py          # Image analysis endpoint
│   │   └── health.py           # Health check
│   └── netlify/functions/      # Netlify functions
│       ├── analyze.py          # ML analysis
│       └── health.py           # Status check
│
└── ⚙️ Configuration
    ├── koyeb.yaml              # Koyeb deployment
    ├── vercel.json             # Vercel serverless
    ├── netlify.toml            # Netlify JAMstack
    └── requirements.txt        # Python dependencies
```

---

## 🧠 Model Information

### Wear Multiclass Model
- **Architecture:** EfficientNetV2-B0 + Custom Classification Head
- **Accuracy:** 72.5% (wear_multiclass_model.h5)
- **Input:** 224x224 RGB images
- **Classes:** Good, Damaged, Severely Damaged
- **Size:** ~170MB (high-performance model)

### Training Details
- **Base Model:** EfficientNetV2-B0 (pre-trained on ImageNet)
- **Fine-tuning:** Custom cookware dataset
- **Optimization:** Model pruning and quantization applied
- **Validation:** Cross-validated on test dataset

---

## 🔌 API Endpoints

### POST /analyze
Analyze cookware condition from uploaded image.

**Request:**
```bash
curl -X POST -F "image=@cookware.jpg" https://your-app.com/analyze
```

**Response:**
```json
{
  "prediction": "Good",
  "confidence": 0.89,
  "all_predictions": {
    "Good": 0.89,
    "Damaged": 0.10,
    "Severely Damaged": 0.01
  }
}
```

### GET /health
Check service status and model availability.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "platform": "koyeb",
  "timestamp": "2023-12-07T10:30:00Z"
}
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Model settings
MODEL_PATH=/models/wear_multiclass_model.h5
NETLIFY_MODEL_PATH=/opt/build/repo/models/wear_multiclass_model.h5

# Environment
ENVIRONMENT=production
DEBUG=false

# Flask settings
FLASK_ENV=production
PYTHONUNBUFFERED=1
TF_CPP_MIN_LOG_LEVEL=2
```

### Platform-Specific Notes

**Koyeb:**
- Uses Gunicorn for production WSGI serving
- Supports WebSocket connections
- Automatic health checks with 60s delay

**Vercel:**
- Serverless functions have 10s timeout
- Automatic edge caching for static assets
- Built-in analytics and monitoring

**Netlify:**
- Functions have 10s timeout (hobby) / 15-26s (pro)
- Built-in form handling and redirects
- Automatic deploy previews for branches

---

## � Performance Tips

### Model Optimization
- Model is pre-optimized (pruning + quantization)
- Uses TensorFlow Lite compatible operations
- Optimized for CPU inference

### Deployment Optimization
- **Koyeb:** Use small instance for cost efficiency
- **Vercel:** Enable edge caching for static assets  
- **Netlify:** Use build plugins for optimization

### Scaling Considerations
- **High Traffic:** Use Koyeb with auto-scaling
- **Variable Load:** Use Vercel serverless functions
- **Static Content:** Use Netlify for optimal CDN caching

---

## 🛠️ Development

### Local Testing
```bash
# Test Flask app
python app.py

# Test Vercel functions
vercel dev

# Test Netlify functions
netlify dev
```

### Model Updates
1. Replace model file in `/models/`
2. Update `MODEL_PATH` in configuration
3. Test with sample images
4. Deploy to your chosen platform

---

## 📊 Platform Comparison

| Feature | Koyeb | Vercel | Netlify |
|---------|-------|--------|---------|
| **Type** | Container/Server | Serverless | JAMstack |
| **Best For** | Production apps | Variable traffic | Static + API |
| **Scaling** | Auto-scaling | Automatic | Functions only |
| **Cold Start** | None | ~1-2s | ~1-2s |
| **Pricing** | Instance-based | Pay-per-request | Build minutes + bandwidth |
| **SSL** | Automatic | Automatic | Automatic |
| **Custom Domain** | ✅ | ✅ | ✅ |
| **WebSockets** | ✅ | ❌ | ❌ |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## � Links

- **Live Demo:** [Deploy on your preferred platform](#quick-deploy)
- **Documentation:** This README
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

---

*Built with ❤️ using TensorFlow, Flask, and modern deployment platforms*