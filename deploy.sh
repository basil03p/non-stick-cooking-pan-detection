#!/bin/bash

# Multi-platform deployment script for Cookware Analyzer
# Supports both Koyeb and Vercel deployments

set -e

echo "🍳 Cookware Analyzer - Multi-Platform Deployment Script"
echo "======================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to deploy to Koyeb
deploy_koyeb() {
    echo "🚀 Deploying to Koyeb..."
    
    if ! command_exists koyeb; then
        echo "❌ Koyeb CLI not found. Installing..."
        curl -fsSL https://cli.koyeb.com/install.sh | sh
        export PATH="$HOME/.koyeb/bin:$PATH"
    fi
    
    echo "📦 Deploying with Koyeb configuration..."
    koyeb app deploy cookware-analyzer --config koyeb.yaml
    
    echo "✅ Koyeb deployment initiated!"
    echo "🔗 Check status: https://app.koyeb.com/"
}

# Function to deploy to Vercel
deploy_vercel() {
    echo "🚀 Deploying to Vercel..."
    
    if ! command_exists vercel; then
        echo "❌ Vercel CLI not found. Installing..."
        npm i -g vercel
    fi
    
    echo "📦 Deploying with Vercel configuration..."
    
    # Copy Vercel-specific requirements
    cp requirements-vercel.txt requirements.txt
    
    # Deploy to Vercel
    vercel deploy --prod
    
    # Restore original requirements
    git checkout requirements.txt 2>/dev/null || echo "No git repo found, keeping Vercel requirements"
    
    echo "✅ Vercel deployment completed!"
    echo "🔗 Your app is now live on Vercel"
}

# Function to deploy to both platforms
deploy_both() {
    echo "🚀 Deploying to both Koyeb and Vercel..."
    
    deploy_koyeb
    echo ""
    deploy_vercel
    
    echo ""
    echo "🎉 Deployment to both platforms completed!"
}

# Function to run pre-deployment checks
pre_deployment_checks() {
    echo "🔍 Running pre-deployment checks..."
    
    # Check if required files exist
    required_files=("app.py" "requirements.txt" "koyeb.yaml" "vercel.json")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            echo "❌ Required file missing: $file"
            exit 1
        fi
    done
    
    # Check if models directory exists
    if [[ ! -d "models" ]]; then
        echo "❌ Models directory not found!"
        exit 1
    fi
    
    # Check if at least one model file exists
    model_count=$(find models -name "*.keras" | wc -l)
    if [[ $model_count -eq 0 ]]; then
        echo "❌ No .keras model files found in models directory!"
        exit 1
    fi
    
    echo "✅ All pre-deployment checks passed!"
}

# Function to show deployment options
show_menu() {
    echo ""
    echo "📋 Deployment Options:"
    echo "1. Deploy to Koyeb only"
    echo "2. Deploy to Vercel only" 
    echo "3. Deploy to both platforms"
    echo "4. Run pre-deployment checks only"
    echo "5. Exit"
    echo ""
}

# Main execution
main() {
    # Run pre-deployment checks first
    pre_deployment_checks
    
    # If arguments provided, use them
    if [[ $# -gt 0 ]]; then
        case $1 in
            "koyeb")
                deploy_koyeb
                ;;
            "vercel")
                deploy_vercel
                ;;
            "both")
                deploy_both
                ;;
            "check")
                echo "✅ Pre-deployment checks completed successfully!"
                ;;
            *)
                echo "❌ Invalid argument. Use: koyeb, vercel, both, or check"
                exit 1
                ;;
        esac
        return
    fi
    
    # Interactive mode
    while true; do
        show_menu
        read -p "Select an option (1-5): " choice
        
        case $choice in
            1)
                deploy_koyeb
                break
                ;;
            2)
                deploy_vercel
                break
                ;;
            3)
                deploy_both
                break
                ;;
            4)
                echo "✅ Pre-deployment checks completed successfully!"
                ;;
            5)
                echo "👋 Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid option. Please select 1-5."
                ;;
        esac
    done
}

# Run the script
main "$@"
