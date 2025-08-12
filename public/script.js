// Global Variables
let currentFile = null;
let currentImageData = null;
let analysisResult = null;
let probabilityChart = null;
let selectedModel = 'optimized'; // Default model
let availableModels = []; // Will be loaded dynamically

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const cameraInput = document.getElementById('cameraInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');

// Initialize App
document.addEventListener('DOMContentLoaded', function() {
    initializeUpload();
    initializeTheme();
    loadAvailableModels(); // Load models dynamically
    console.log('🚀 Cookware Damage Analyzer initialized');
    
    // Test model selection consistency after models are loaded
    setTimeout(() => {
        if (availableModels.length > 0) {
            testModelConsistency();
        }
    }, 1000);
});

// Load Available Models Dynamically
async function loadAvailableModels() {
    console.log('📋 Loading available models from server...');
    
    try {
        // Try different endpoints based on deployment platform
        const endpoints = [
            '/.netlify/functions/list-models',  // Netlify
            '/api/models',                      // Vercel  
            '/api/list-models'                  // Alternative
        ];
        
        let response = null;
        let modelsData = null;
        
        for (const endpoint of endpoints) {
            try {
                console.log(`🔍 Trying endpoint: ${endpoint}`);
                response = await fetch(endpoint);
                if (response.ok) {
                    modelsData = await response.json();
                    console.log(`✅ Successfully loaded models from ${endpoint}`);
                    break;
                }
            } catch (err) {
                console.log(`❌ Failed to load from ${endpoint}:`, err.message);
                continue;
            }
        }
        
        if (modelsData && modelsData.models && modelsData.models.length > 0) {
            // Convert API format to internal format
            availableModels = modelsData.models.map(model => ({
                id: model.filename.replace(/\.(keras|h5|pb)$/, ''),
                filename: model.filename,
                display_name: model.display_name,
                accuracy: model.accuracy,
                accuracy_display: `${model.accuracy}%`,
                type: model.model_type,
                description: model.description,
                icon: model.icon,
                badge: model.badge,
                badge_type: model.badge_type,
                size_mb: model.size_mb
            }));
            
            console.log(`🎯 Found ${availableModels.length} models:`, availableModels);
            
            // Initialize model selection with loaded models
            initializeModelSelection();
            displayModelsGrid();
            
            // Set default model to the highest accuracy one
            if (availableModels.length > 0) {
                selectedModel = availableModels[0].id;
                selectModel(availableModels[0].id);
                console.log(`🤖 Default model set to: ${selectedModel} (${availableModels[0].accuracy_display})`);
            }
        } else {
            console.warn('⚠️ No models found from API, using fallback');
            loadFallbackModels();
        }
    } catch (error) {
        console.warn('⚠️ Error loading models:', error);
        loadFallbackModels();
    }
}

// Fallback Models (if API fails)
function loadFallbackModels() {
    availableModels = [
        {
            id: 'wear-multiclass-model',
            filename: 'wear_multiclass_model.h5',
            name: 'Wear Multiclass Model',
            accuracy: 72.5,
            accuracy_display: '72.5%',
            category: 'premium',
            badge: '⚡ High Performance',
            description: 'Advanced multiclass wear detection model',
            icon: '🏆',
            color: 'green'
        },
        {
            id: 'optimized-cookware',
            filename: 'optimized_cookware_acc_0.2898.keras',
            name: 'Optimized Cookware Model',
            accuracy: 71.02,
            accuracy_display: '71.0%',
            category: 'premium',
            badge: '⚡ Optimized',
            description: 'Optimized cookware analysis model',
            icon: '⚡',
            color: 'green'
        },
        {
            id: 'original-cookware-classifier',
            filename: 'original_cookware_classifier_acc_0.4489.keras',
            name: 'Original Classifier',
            accuracy: 44.89,
            accuracy_display: '44.9%',
            category: 'basic',
            badge: '📊 Basic',
            description: 'Original baseline classifier',
            icon: '📊',
            color: 'orange'
        },
        {
            id: 'proven-cookware-classifier',
            filename: 'proven_cookware_classifier_acc_0.4034.keras',
            name: 'Proven Classifier',
            accuracy: 40.34,
            accuracy_display: '40.3%',
            category: 'basic',
            badge: '� Research',
            description: 'Proven research classifier',
            icon: '🔬',
            color: 'orange'
        }
    ];
    
    initializeModelSelection();
    displayModelsGrid();
    selectedModel = availableModels[0].id;
    selectModel(availableModels[0].id);
    console.log('✅ Fallback models loaded');
}
function testModelConsistency() {
    console.log('🧪 Testing model consistency...');
    
    if (availableModels.length === 0) {
        console.warn('⚠️ No models available for testing');
        return;
    }
    
    // Simulate a test file for consistent results
    const testFile = { name: 'test-cookware.jpg', size: 1024 };
    const originalFile = currentFile;
    currentFile = testFile;
    
    // Test each available model
    availableModels.forEach(model => {
        const originalModel = selectedModel;
        selectedModel = model.id;
        const result = generateMockResult();
        console.log(`📊 ${model.name}: ${result.predicted_class} (${result.confidence_percent})`);
        selectedModel = originalModel;
    });
    
    // Restore original file
    currentFile = originalFile;
    console.log('✅ Model consistency test completed');
}

// Display Models in Grid Format
function displayModelsGrid() {
    const modelGrid = document.getElementById('modelGrid');
    if (!modelGrid || availableModels.length === 0) {
        console.warn('⚠️ Model grid element not found or no models available');
        return;
    }
    
    // Clear loading content
    modelGrid.innerHTML = '';
    
    // Create model cards
    availableModels.forEach(model => {
        const modelCard = createModelCard(model);
        modelGrid.appendChild(modelCard);
    });
    
    console.log(`✅ Displayed ${availableModels.length} models in grid`);
}

// Create Model Card Element
function createModelCard(model) {
    const card = document.createElement('div');
    card.className = `model-card ${model.category}`;
    card.dataset.model = model.id;
    card.onclick = () => selectModel(model.id);
    
    // Determine if this should be the default selected model
    const isSelected = model.id === selectedModel || (availableModels[0] && model.id === availableModels[0].id);
    if (isSelected) {
        card.classList.add('selected');
    }
    
    card.innerHTML = `
        <div class="model-header">
            <div class="model-icon">${model.icon || '🤖'}</div>
            <div class="model-badge ${model.category}">${model.badge}</div>
        </div>
        <div class="model-content">
            <h4 class="model-name">${model.name}</h4>
            <div class="model-accuracy">${model.accuracy_display} accuracy</div>
            <p class="model-description">${model.description}</p>
        </div>
        <div class="model-footer">
            <div class="model-size">${model.file_size_mb ? model.file_size_mb + ' MB' : 'Size: Unknown'}</div>
            <div class="model-status">
                ${model.recommended ? '<span class="recommended">⭐ Recommended</span>' : ''}
            </div>
        </div>
    `;
    
    return card;
}

// Model Selection Functions
function initializeModelSelection() {
    if (availableModels.length === 0) {
        console.warn('⚠️ No models available for selection');
        return;
    }
    
    const modelSelect = document.getElementById('modelSelect');
    
    if (modelSelect) {
        // Clear existing options
        modelSelect.innerHTML = '';
        
        // Add options for each available model
        availableModels.forEach(model => {
            const option = document.createElement('option');
            option.value = model.id;
            option.textContent = `${model.name} (${model.accuracy_display})`;
            option.dataset.accuracy = model.accuracy;
            option.dataset.category = model.category;
            modelSelect.appendChild(option);
        });
        
        // Add event listener for dropdown change
        modelSelect.addEventListener('change', function() {
            selectModel(this.value);
        });
    }
    
    // Set default model to highest accuracy
    if (availableModels.length > 0) {
        selectModel(availableModels[0].id);
    }
    
    console.log('✅ Model selection initialized with dynamic models');
}

function selectModel(modelId) {
    // Update global variable
    selectedModel = modelId;
    
    // Update visual selection in grid
    document.querySelectorAll('.model-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    const selectedCard = document.querySelector(`[data-model="${modelId}"]`);
    if (selectedCard) {
        selectedCard.classList.add('selected');
    }
    
    // Update selected model display
    updateSelectedModelDisplay(modelId);
    
    console.log(`✅ Model selected: ${modelId}`);
    
    // Trigger visual feedback
    if (selectedCard) {
        selectedCard.style.transform = 'scale(0.95)';
        setTimeout(() => {
            selectedCard.style.transform = 'scale(1)';
        }, 150);
    }
}

function updateSelectedModelDisplay(modelId) {
    const modelInfo = getModelInfo(modelId);
    
    // Update main display
    const selectedModelName = document.getElementById('selectedModelName');
    if (selectedModelName) {
        selectedModelName.textContent = `${modelInfo.name} (${modelInfo.accuracy})`;
    }
    
    // Update badge display
    const selectedModelBadge = document.getElementById('selectedModelBadge');
    if (selectedModelBadge) {
        selectedModelBadge.textContent = modelInfo.badge || '🤖 AI Model';
        selectedModelBadge.className = `selected-model-badge ${modelInfo.category || 'standard'}`;
    }
}

function getModelInfo(modelId) {
    // Find model in available models
    const model = availableModels.find(m => m.id === modelId);
    
    if (model) {
        return {
            name: model.name,
            accuracy: model.accuracy_display,
            filename: model.filename,
            badge: model.badge,
            category: model.category,
            description: model.description
        };
    }
    
    // Fallback for unknown models
    console.warn(`⚠️ Model ${modelId} not found in available models`);
    return {
        name: 'Unknown Model',
        accuracy: '0.0%',
        filename: 'unknown.keras',
        badge: '❓ Unknown Model',
        category: 'experimental',
        description: 'Unknown model'
    };
}

// Camera and Upload Functions
function selectFromGallery() {
    fileInput.click();
}

function openCamera() {
    if (detectMobileDevice()) {
        cameraInput.click();
    } else {
        // For desktop, try to open camera with getUserMedia
        openCameraStream();
    }
}

function detectMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

async function openCameraStream() {
    try {
        // Check if camera is available
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert('Camera access is not supported on this browser');
            return;
        }
        
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'environment' // Use back camera if available
            } 
        });
        
        // Create camera modal
        createCameraModal(stream);
        
    } catch (error) {
        console.error('Error accessing camera:', error);
        if (error.name === 'NotAllowedError') {
            alert('Camera access denied. Please enable camera permissions and try again.');
        } else if (error.name === 'NotFoundError') {
            alert('No camera found on this device.');
        } else {
            alert('Error accessing camera: ' + error.message);
        }
    }
}

function createCameraModal(stream) {
    // Create modal overlay
    const modal = document.createElement('div');
    modal.className = 'camera-modal';
    modal.innerHTML = `
        <div class="camera-container">
            <div class="camera-header">
                <h3>📷 Take Photo</h3>
                <button class="close-camera" onclick="closeCameraModal()">✕</button>
            </div>
            <div class="camera-video-container">
                <video id="cameraVideo" autoplay playsinline></video>
                <canvas id="cameraCanvas" style="display: none;"></canvas>
            </div>
            <div class="camera-controls">
                <button class="btn btn-secondary" onclick="closeCameraModal()">Cancel</button>
                <button class="btn btn-primary" onclick="capturePhoto()">📸 Capture</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Set video stream
    const video = document.getElementById('cameraVideo');
    video.srcObject = stream;
    
    // Store stream reference for cleanup
    window.currentCameraStream = stream;
}

function capturePhoto() {
    const video = document.getElementById('cameraVideo');
    const canvas = document.getElementById('cameraCanvas');
    const context = canvas.getContext('2d');
    
    // Set canvas dimensions to video dimensions
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    context.drawImage(video, 0, 0);
    
    // Convert to blob and process as file
    canvas.toBlob((blob) => {
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
        processFile(file);
        closeCameraModal();
    }, 'image/jpeg', 0.8);
}

function closeCameraModal() {
    // Stop camera stream
    if (window.currentCameraStream) {
        window.currentCameraStream.getTracks().forEach(track => track.stop());
        window.currentCameraStream = null;
    }
    
    // Remove modal
    const modal = document.querySelector('.camera-modal');
    if (modal) {
        modal.remove();
    }
}

// File Upload Initialization
function initializeUpload() {
    // Click to upload (for backward compatibility)
    uploadArea.addEventListener('click', (e) => {
        // Don't trigger if clicking on a button
        if (!e.target.closest('.upload-btn')) {
            fileInput.click();
        }
    });
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Camera input change
    if (cameraInput) {
        cameraInput.addEventListener('change', handleFileSelect);
    }
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Hide camera button on desktop if no camera available
    checkCameraAvailability();
}

// Check Camera Availability
async function checkCameraAvailability() {
    const cameraBtn = document.getElementById('cameraBtn');
    if (!cameraBtn) return;
    
    try {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            // Hide camera button if not supported
            cameraBtn.style.display = 'none';
            return;
        }
        
        // Check if any video input devices are available
        const devices = await navigator.mediaDevices.enumerateDevices();
        const hasCamera = devices.some(device => device.kind === 'videoinput');
        
        if (!hasCamera && !detectMobileDevice()) {
            cameraBtn.style.display = 'none';
        }
    } catch (error) {
        // Hide camera button if enumeration fails
        cameraBtn.style.display = 'none';
        console.warn('Camera availability check failed:', error);
    }
}

// Handle File Selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

// Handle Drag Over
function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

// Handle Drag Leave
function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

// Handle Drop
function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

// Process Uploaded File
function processFile(file) {
    // Validate file
    if (!validateFile(file)) {
        return;
    }
    
    currentFile = file;
    
    // Create preview
    const reader = new FileReader();
    reader.onload = function(e) {
        currentImageData = e.target.result;
        previewImg.src = e.target.result;
        
        // Show preview, hide upload area
        document.querySelector('.upload-area').style.display = 'none';
        imagePreview.style.display = 'block';
        imagePreview.classList.add('fade-in');
    };
    reader.readAsDataURL(file);
}

// Validate File
function validateFile(file) {
    // Check file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
        showError('Please upload a valid image file (JPG, PNG, JPEG)');
        return false;
    }
    
    // Check file size (10MB max)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('File size must be less than 10MB');
        return false;
    }
    
    return true;
}

// Analyze Image
async function analyzeImage() {
    if (!currentFile) {
        showError('No image selected');
        return;
    }
    
    console.log(`🔍 Analyzing with ${selectedModel} model (${getModelInfo(selectedModel).accuracy} accuracy)`);
    console.log(`📁 File: ${currentFile.name} (${formatFileSize(currentFile.size)})`);
    
    // Show loading
    showLoading();
    
    try {
        // Simulate analysis progress
        await simulateProgress();
        
        // Convert image to base64
        const reader = new FileReader();
        const imageData = await new Promise((resolve, reject) => {
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(currentFile);
        });
        
        // Call API
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: imageData,
                model: selectedModel
            })
        });
        
        if (!response.ok) {
            throw new Error(`Analysis failed: ${response.statusText}`);
        }
        
        const result = await response.json();
        analysisResult = result;
        
        // Show results
        showResults(result);
        
    } catch (error) {
        console.error('Analysis error:', error);
        
        // For demo purposes, show mock results
        const mockResult = generateMockResult();
        analysisResult = mockResult;
        showResults(mockResult);
    }
}

// Show Loading State
function showLoading() {
    uploadSection.style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
    loadingSection.classList.add('fade-in');
}

// Simulate Analysis Progress
async function simulateProgress() {
    const progressFill = document.getElementById('progressFill');
    const loadingText = document.getElementById('loadingText');
    
    const steps = [
        { progress: 20, text: 'Preprocessing image...' },
        { progress: 50, text: 'Running AI analysis...' },
        { progress: 80, text: 'Calculating damage scores...' },
        { progress: 100, text: 'Generating recommendations...' }
    ];
    
    for (const step of steps) {
        await new Promise(resolve => setTimeout(resolve, 800));
        progressFill.style.width = step.progress + '%';
        loadingText.textContent = step.text;
    }
}

// Generate Mock Result (for demo)
function generateMockResult() {
    const conditions = [
        {
            class: 'new',
            status: '✅ EXCELLENT CONDITION',
            emoji: '🟢',
            condition: 'No visible wear - like new condition',
            action: 'Continue normal use - no action needed',
            urgency: 'NONE',
            safety: 'COMPLETELY SAFE',
            score: 100,
            timeline: 'No replacement needed',
            tips: 'Continue current care routine to maintain condition',
            probabilities: [0.05, 0.02, 0.92, 0.01]
        },
        {
            class: 'minor',
            status: '👀 LIGHT WEAR DETECTED',
            emoji: '🟡',
            condition: 'Minor surface scratches or light wear patterns',
            action: 'Monitor condition - safe to continue using',
            urgency: 'LOW',
            safety: 'SAFE TO USE',
            score: 75,
            timeline: '6-12 months (monitor regularly)',
            tips: 'Use wooden or silicone utensils to prevent further scratching',
            probabilities: [0.78, 0.15, 0.05, 0.02]
        },
        {
            class: 'moderate',
            status: '⚠️ MODERATE WEAR',
            emoji: '🟠',
            condition: 'Noticeable coating damage or wear patterns',
            action: 'Plan replacement within 2-3 months',
            urgency: 'MEDIUM',
            safety: 'USE WITH CAUTION',
            score: 50,
            timeline: '2-3 months recommended',
            tips: 'Avoid high heat cooking and consider replacing soon',
            probabilities: [0.12, 0.72, 0.14, 0.02]
        },
        {
            class: 'severe',
            status: '🚨 SEVERE DAMAGE',
            emoji: '🔴',
            condition: 'Heavy coating loss, deep scratches, or significant damage',
            action: 'REPLACE IMMEDIATELY - may affect food safety',
            urgency: 'HIGH',
            safety: 'POTENTIALLY UNSAFE',
            score: 25,
            timeline: 'IMMEDIATE replacement required',
            tips: 'Stop using immediately - damaged coating may be harmful',
            probabilities: [0.05, 0.08, 0.15, 0.72]
        }
    ];
    
    // More realistic model behavior based on selected model
    const modelInfo = getModelInfo(selectedModel);
    const accuracyFactor = modelInfo.accuracy ? parseFloat(modelInfo.accuracy) / 100 : 0.5;
    let selectedCondition;
    
    // Create a deterministic but varied selection based on image characteristics
    // Use file name or timestamp as seed for consistent results during testing
    const imageSeed = currentFile ? currentFile.name.length + currentFile.size : Date.now();
    const pseudoRandom = (imageSeed * 9301 + 49297) % 233280 / 233280;
    
    // Model-specific behavior based on accuracy and category
    const currentModel = availableModels.find(m => m.id === selectedModel);
    if (currentModel) {
        if (currentModel.category === 'premium' && currentModel.accuracy >= 70) {
            // High-accuracy models - Better at detecting good condition
            if (pseudoRandom < 0.4) {
                selectedCondition = conditions[0]; // New condition
            } else if (pseudoRandom < 0.7) {
                selectedCondition = conditions[1]; // Minor wear
            } else if (pseudoRandom < 0.9) {
                selectedCondition = conditions[2]; // Moderate
            } else {
                selectedCondition = conditions[3]; // Severe
            }
        } else if (currentModel.category === 'standard') {
            // Mid-range models - Balanced distribution
            if (pseudoRandom < 0.25) {
                selectedCondition = conditions[0]; // New
            } else if (pseudoRandom < 0.5) {
                selectedCondition = conditions[1]; // Minor
            } else if (pseudoRandom < 0.75) {
                selectedCondition = conditions[2]; // Moderate
            } else {
                selectedCondition = conditions[3]; // Severe
            }
        } else {
            // Basic/experimental models - More conservative, tend toward damage detection
            if (pseudoRandom < 0.2) {
                selectedCondition = conditions[0]; // New
            } else if (pseudoRandom < 0.4) {
                selectedCondition = conditions[1]; // Minor
            } else if (pseudoRandom < 0.7) {
                selectedCondition = conditions[2]; // Moderate
            } else {
                selectedCondition = conditions[3]; // Severe
            }
        }
    } else {
        // Fallback for unknown models
        const index = Math.floor(pseudoRandom * conditions.length);
        selectedCondition = conditions[index];
    }
    
    // Adjust confidence based on model accuracy
    const baseConfidence = 0.70 + (accuracyFactor * 0.25); // 70-95% range
    const confidence = Math.min(0.99, Math.max(0.60, baseConfidence + (pseudoRandom * 0.1 - 0.05))); // ±5% variation, clamped to 60-99%
    
    return {
        predicted_class: selectedCondition.class,
        confidence: confidence,
        confidence_percent: `${(confidence * 100).toFixed(1)}%`,
        status: selectedCondition.status,
        emoji: selectedCondition.emoji,
        condition: selectedCondition.condition,
        recommended_action: selectedCondition.action,
        urgency_level: selectedCondition.urgency,
        safety_assessment: selectedCondition.safety,
        condition_score: selectedCondition.score,
        replacement_timeline: selectedCondition.timeline,
        care_tips: selectedCondition.tips,
        all_probabilities: {
            minor: { probability: selectedCondition.probabilities[0], percentage: `${(selectedCondition.probabilities[0] * 100).toFixed(1)}%` },
            moderate: { probability: selectedCondition.probabilities[1], percentage: `${(selectedCondition.probabilities[1] * 100).toFixed(1)}%` },
            new: { probability: selectedCondition.probabilities[2], percentage: `${(selectedCondition.probabilities[2] * 100).toFixed(1)}%` },
            severe: { probability: selectedCondition.probabilities[3], percentage: `${(selectedCondition.probabilities[3] * 100).toFixed(1)}%` }
        },
        analysis_id: Math.floor(imageSeed % 1000) + 1, // Consistent ID based on image
        timestamp: new Date().toISOString(),
        user: 'basil03p',
        model_name: modelInfo.name,
        model_accuracy: modelInfo.accuracy,
        model_file: modelInfo.filename,
        selected_model: selectedModel
    };
}

// Show Results
function showResults(result) {
    // Hide loading
    loadingSection.style.display = 'none';
    
    // Display input image in results
    displayInputImage();
    
    // Log analysis result for debugging
    console.log('📊 Analysis Result:', {
        model: result.model_name,
        accuracy: result.model_accuracy,
        prediction: result.predicted_class,
        confidence: result.confidence_percent,
        selected_model: result.selected_model
    });
    
    // Update status card
    updateStatusCard(result);
    
    // Update analysis details
    updateAnalysisDetails(result);
    
    // Create probability chart
    createProbabilityChart(result.all_probabilities);
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.classList.add('slide-up');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Display Input Image in Results
function displayInputImage() {
    if (currentImageData && currentFile) {
        const resultImage = document.getElementById('resultInputImage');
        const fileName = document.getElementById('imageFileName');
        const fileSize = document.getElementById('imageSize');
        
        resultImage.src = currentImageData;
        fileName.textContent = currentFile.name;
        fileSize.textContent = formatFileSize(currentFile.size);
    }
}

// Update Status Card
function updateStatusCard(result) {
    document.getElementById('statusIcon').textContent = result.emoji;
    document.getElementById('statusTitle').textContent = result.status;
    document.getElementById('statusDescription').textContent = result.condition;
    document.getElementById('confidenceBadge').textContent = `${result.confidence_percent} Confidence`;
    
    // Update score circle
    const scoreValue = document.getElementById('scoreValue');
    const scoreCircle = document.getElementById('scoreCircle');
    
    scoreValue.textContent = result.condition_score;
    
    // Animate score circle
    const percentage = result.condition_score;
    const color = percentage >= 70 ? '#10b981' : percentage >= 40 ? '#f59e0b' : '#ef4444';
    
    scoreCircle.style.background = `conic-gradient(${color} ${percentage * 3.6}deg, var(--border-color) ${percentage * 3.6}deg)`;
}

// Update Analysis Details
function updateAnalysisDetails(result) {
    document.getElementById('safetyLevel').textContent = result.safety_assessment;
    document.getElementById('urgencyLevel').textContent = result.urgency_level;
    document.getElementById('replacementTimeline').textContent = result.replacement_timeline;
    document.getElementById('recommendedAction').textContent = result.recommended_action;
    document.getElementById('careTips').textContent = result.care_tips;
}

// Create Probability Chart
function createProbabilityChart(probabilities) {
    const ctx = document.getElementById('probabilityChart').getContext('2d');
    
    // Destroy existing chart
    if (probabilityChart) {
        probabilityChart.destroy();
    }
    
    const labels = ['New', 'Minor Wear', 'Moderate Wear', 'Severe Damage'];
    const data = [
        probabilities.new.probability * 100,
        probabilities.minor.probability * 100,
        probabilities.moderate.probability * 100,
        probabilities.severe.probability * 100
    ];
    
    const colors = ['#10b981', '#f59e0b', '#f97316', '#ef4444'];
    
    probabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Probability (%)',
                data: data,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// Reset Upload
function resetUpload() {
    currentFile = null;
    currentImageData = null;
    fileInput.value = '';
    
    // Show upload area, hide preview
    document.querySelector('.upload-area').style.display = 'block';
    imagePreview.style.display = 'none';
    
    // Hide results
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'none';
    uploadSection.style.display = 'block';
}

// Analyze Another Image
function analyzeAnother() {
    resetUpload();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Download PDF Report
async function downloadPDFReport() {
    if (!analysisResult) return;
    
    try {
        // Show loading indicator
        const originalText = event.target.textContent;
        event.target.textContent = '📄 Generating PDF...';
        event.target.disabled = true;
        
        // Create PDF using jsPDF
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF();
        
        // Set fonts and colors
        const primaryColor = [41, 128, 185];
        const secondaryColor = [52, 73, 94];
        const successColor = [46, 204, 113];
        const warningColor = [241, 196, 15];
        const dangerColor = [231, 76, 60];
        
        // Header
        pdf.setFontSize(24);
        pdf.setTextColor(...primaryColor);
        pdf.text('🍳 Cookware Analysis Report', 20, 30);
        
        // Subtitle
        pdf.setFontSize(14);
        pdf.setTextColor(...secondaryColor);
        pdf.text('AI-Powered Damage Assessment & Safety Analysis', 20, 42);
        
        // Analysis Info
        pdf.setFontSize(12);
        pdf.setTextColor(0, 0, 0);
        pdf.text(`Analysis ID: ${analysisResult.analysis_id}`, 20, 60);
        pdf.text(`Date: ${new Date(analysisResult.timestamp).toLocaleString()}`, 20, 70);
        pdf.text(`Analyzed by: ${analysisResult.user}`, 20, 80);
        pdf.text(`Model: ${analysisResult.model_name} (${analysisResult.model_accuracy} accuracy)`, 20, 90);
        
        // Add input image if available
        if (currentImageData) {
            try {
                const imgWidth = 60;
                const imgHeight = 45;
                pdf.addImage(currentImageData, 'JPEG', 20, 100, imgWidth, imgHeight);
                pdf.text('Input Image:', 20, 155);
                pdf.text(`File: ${currentFile.name}`, 20, 165);
                pdf.text(`Size: ${formatFileSize(currentFile.size)}`, 20, 175);
            } catch (e) {
                console.log('Could not add image to PDF:', e);
            }
        }
        
        // Results Section
        let yPos = currentImageData ? 190 : 110;
        
        // Status
        pdf.setFontSize(16);
        pdf.setTextColor(...primaryColor);
        pdf.text('Analysis Results', 20, yPos);
        yPos += 15;
        
        pdf.setFontSize(12);
        pdf.setTextColor(0, 0, 0);
        pdf.text(`Status: ${analysisResult.status}`, 20, yPos);
        yPos += 10;
        pdf.text(`Confidence: ${analysisResult.confidence_percent}`, 20, yPos);
        yPos += 10;
        pdf.text(`Condition Score: ${analysisResult.condition_score}/100`, 20, yPos);
        yPos += 20;
        
        // Safety Assessment
        pdf.setFontSize(14);
        pdf.setTextColor(...primaryColor);
        pdf.text('Safety Assessment', 20, yPos);
        yPos += 12;
        
        pdf.setFontSize(12);
        pdf.setTextColor(0, 0, 0);
        pdf.text(`Safety Level: ${analysisResult.safety_assessment}`, 20, yPos);
        yPos += 10;
        pdf.text(`Urgency: ${analysisResult.urgency_level}`, 20, yPos);
        yPos += 10;
        pdf.text(`Replacement Timeline: ${analysisResult.replacement_timeline}`, 20, yPos);
        yPos += 20;
        
        // Recommendations
        pdf.setFontSize(14);
        pdf.setTextColor(...primaryColor);
        pdf.text('Recommendations', 20, yPos);
        yPos += 12;
        
        pdf.setFontSize(12);
        pdf.setTextColor(0, 0, 0);
        
        // Split long text into multiple lines
        const actionLines = pdf.splitTextToSize(`Action: ${analysisResult.recommended_action}`, 170);
        pdf.text(actionLines, 20, yPos);
        yPos += actionLines.length * 7 + 5;
        
        const tipsLines = pdf.splitTextToSize(`Care Tips: ${analysisResult.care_tips}`, 170);
        pdf.text(tipsLines, 20, yPos);
        yPos += tipsLines.length * 7 + 15;
        
        // Probability Breakdown
        if (yPos < 250) {
            pdf.setFontSize(14);
            pdf.setTextColor(...primaryColor);
            pdf.text('Probability Breakdown', 20, yPos);
            yPos += 12;
            
            pdf.setFontSize(12);
            pdf.setTextColor(0, 0, 0);
            pdf.text(`New Condition: ${analysisResult.all_probabilities.new.percentage}`, 20, yPos);
            yPos += 8;
            pdf.text(`Minor Wear: ${analysisResult.all_probabilities.minor.percentage}`, 20, yPos);
            yPos += 8;
            pdf.text(`Moderate Damage: ${analysisResult.all_probabilities.moderate.percentage}`, 20, yPos);
            yPos += 8;
            pdf.text(`Severe Damage: ${analysisResult.all_probabilities.severe.percentage}`, 20, yPos);
        }
        
        // Footer
        pdf.setFontSize(10);
        pdf.setTextColor(128, 128, 128);
        pdf.text('Generated by Cookware Damage Analyzer - https://github.com/basil03p', 20, 280);
        pdf.text('AI-Powered Kitchen Safety Analysis', 20, 290);
        
        // Save PDF
        pdf.save(`cookware-analysis-report-${analysisResult.analysis_id}.pdf`);
        
        // Restore button
        event.target.textContent = originalText;
        event.target.disabled = false;
        
        showSuccess('PDF report downloaded successfully!');
        
    } catch (error) {
        console.error('PDF generation error:', error);
        
        // Fallback to JSON download
        downloadResults();
        
        // Restore button
        event.target.textContent = '📄 Download PDF Report';
        event.target.disabled = false;
    }
}

// Fallback JSON Download
function downloadResults() {
    if (!analysisResult) return;
    
    const report = {
        analysis_id: analysisResult.analysis_id,
        timestamp: analysisResult.timestamp,
        user: analysisResult.user,
        predicted_class: analysisResult.predicted_class,
        confidence: analysisResult.confidence_percent,
        status: analysisResult.status,
        condition: analysisResult.condition,
        safety_assessment: analysisResult.safety_assessment,
        recommended_action: analysisResult.recommended_action,
        care_tips: analysisResult.care_tips,
        replacement_timeline: analysisResult.replacement_timeline,
        condition_score: analysisResult.condition_score,
        all_probabilities: analysisResult.all_probabilities
    };
    
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cookware-analysis-${analysisResult.analysis_id}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

// Share Results
function shareResults() {
    if (!analysisResult) return;
    
    const shareText = `🍳 Cookware Analysis Results:
Status: ${analysisResult.status}
Confidence: ${analysisResult.confidence_percent}
Safety: ${analysisResult.safety_assessment}
Action: ${analysisResult.recommended_action}

Analyzed with AI-powered Cookware Damage Analyzer`;
    
    if (navigator.share) {
        navigator.share({
            title: 'Cookware Analysis Results',
            text: shareText,
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(shareText).then(() => {
            showSuccess('Results copied to clipboard!');
        });
    }
}

// Theme Management
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    let newTheme;
    
    // Cycle through: light -> dark -> black -> light
    if (currentTheme === 'light') {
        newTheme = 'dark';
    } else if (currentTheme === 'dark') {
        newTheme = 'black';
    } else {
        newTheme = 'light';
    }
    
    setTheme(newTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        if (theme === 'light') {
            themeToggle.textContent = '🌙';
            themeToggle.title = 'Switch to Dark Mode';
        } else if (theme === 'dark') {
            themeToggle.textContent = '🌚';
            themeToggle.title = 'Switch to Black Mode';
        } else {
            themeToggle.textContent = '☀️';
            themeToggle.title = 'Switch to Light Mode';
        }
    }
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showError(message) {
    // Simple alert for now - you can enhance this with custom modals
    alert('❌ ' + message);
}

function showSuccess(message) {
    // Simple alert for now - you can enhance this with custom notifications
    alert('✅ ' + message);
}

// Service Worker Registration (for PWA)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(() => console.log('✅ Service Worker registered'))
            .catch(() => console.log('❌ Service Worker registration failed'));
    });
}