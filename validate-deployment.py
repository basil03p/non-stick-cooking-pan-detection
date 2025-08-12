#!/usr/bin/env python3
"""
Triple Platform Deployment Validation Script
Validates Koyeb, Vercel, and Netlify deployment configurations
"""

import os
import json
import sys
from pathlib import Path

class DeploymentValidator:
    def __init__(self):
        self.root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        
    def validate_file_exists(self, filepath, platform=""):
        """Check if a file exists and is readable"""
        full_path = self.root / filepath
        if not full_path.exists():
            self.errors.append(f"❌ Missing: {filepath} ({platform})")
            return False
        
        if full_path.stat().st_size == 0:
            self.warnings.append(f"⚠️  Empty file: {filepath} ({platform})")
            
        print(f"✅ Found: {filepath} ({platform})")
        return True
    
    def validate_json_file(self, filepath, required_keys=None):
        """Validate JSON file structure"""
        if not self.validate_file_exists(filepath):
            return False
            
        try:
            with open(self.root / filepath, 'r') as f:
                data = json.load(f)
                
            if required_keys:
                missing = [key for key in required_keys if key not in data]
                if missing:
                    self.errors.append(f"❌ Missing keys in {filepath}: {missing}")
                    return False
                    
            print(f"✅ Valid JSON: {filepath}")
            return True
            
        except json.JSONDecodeError as e:
            self.errors.append(f"❌ Invalid JSON in {filepath}: {e}")
            return False
    
    def validate_python_syntax(self, filepath):
        """Basic Python syntax validation"""
        if not self.validate_file_exists(filepath):
            return False
            
        try:
            with open(self.root / filepath, 'r') as f:
                content = f.read()
                compile(content, filepath, 'exec')
            print(f"✅ Valid Python: {filepath}")
            return True
            
        except SyntaxError as e:
            self.errors.append(f"❌ Python syntax error in {filepath}: {e}")
            return False
    
    def validate_koyeb(self):
        """Validate Koyeb deployment configuration"""
        print("\n🚀 Validating Koyeb Configuration...")
        
        # Check main app file
        self.validate_python_syntax("app.py")
        
        # Check koyeb.yaml
        if self.validate_file_exists("koyeb.yaml", "Koyeb"):
            # Additional YAML validation could be added here
            pass
            
        # Check requirements
        self.validate_file_exists("requirements.txt", "Koyeb")
        
        # Check model file
        self.validate_file_exists("models/wear_multiclass_model.h5", "Koyeb")
        
        print("✅ Koyeb configuration validated")
    
    def validate_vercel(self):
        """Validate Vercel deployment configuration"""
        print("\n⚡ Validating Vercel Configuration...")
        
        # Check vercel.json
        self.validate_json_file("vercel.json", ["functions", "routes"])
        
        # Check API functions
        self.validate_python_syntax("api/analyze.py")
        self.validate_python_syntax("api/health.py")
        
        # Check requirements
        self.validate_file_exists("requirements.txt", "Vercel")
        
        print("✅ Vercel configuration validated")
    
    def validate_netlify(self):
        """Validate Netlify deployment configuration"""
        print("\n🌐 Validating Netlify Configuration...")
        
        # Check netlify.toml
        if self.validate_file_exists("netlify.toml", "Netlify"):
            # Additional TOML validation could be added here
            pass
            
        # Check Netlify functions
        self.validate_python_syntax("netlify/functions/analyze.py")
        self.validate_python_syntax("netlify/functions/health.py")
        
        # Check public directory
        self.validate_file_exists("public/index.html", "Netlify")
        self.validate_file_exists("public/script.js", "Netlify")
        self.validate_file_exists("public/styles.css", "Netlify")
        
        print("✅ Netlify configuration validated")
    
    def validate_common_files(self):
        """Validate files common to all platforms"""
        print("\n📁 Validating Common Files...")
        
        # Check model exists
        if not self.validate_file_exists("models/wear_multiclass_model.h5"):
            self.errors.append("❌ Critical: ML model file missing!")
            
        # Check frontend files
        self.validate_file_exists("public/index.html")
        self.validate_file_exists("public/script.js")
        self.validate_file_exists("public/styles.css")
        
        # Check documentation
        self.validate_file_exists("README.md")
        
        # Check environment file
        if self.validate_file_exists(".env.local"):
            print("✅ Environment configuration found")
    
    def generate_deployment_commands(self):
        """Generate platform-specific deployment commands"""
        print("\n🔧 Deployment Commands:")
        
        print("\n📋 Koyeb Deployment:")
        print("   1. Connect repository to Koyeb dashboard")
        print("   2. Use build command: pip install -r requirements.txt")
        print("   3. Use run command: gunicorn app:app --bind 0.0.0.0:$PORT")
        print("   4. Set health check: /health")
        
        print("\n📋 Vercel Deployment:")
        print("   1. npm i -g vercel")
        print("   2. vercel --prod")
        print("   3. Follow prompts for configuration")
        
        print("\n📋 Netlify Deployment:")
        print("   1. npm install -g netlify-cli")
        print("   2. netlify init")
        print("   3. netlify build")
        print("   4. netlify deploy --prod")
        print("   5. Or connect repository in Netlify dashboard")
        
        print("\n📋 Build Settings for Netlify Dashboard:")
        print("   • Build command: pip install -r requirements.txt")
        print("   • Publish directory: public")
        print("   • Functions directory: netlify/functions")
    
    def run_validation(self):
        """Run complete validation suite"""
        print("🔍 Triple Platform Deployment Validation")
        print("=" * 50)
        
        self.validate_common_files()
        self.validate_koyeb()
        self.validate_vercel()
        self.validate_netlify()
        
        print("\n" + "=" * 50)
        print("📊 Validation Summary:")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")
                
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
                
        if not self.errors and not self.warnings:
            print("\n🎉 All validations passed!")
            print("✅ Ready for deployment on all platforms")
        elif not self.errors:
            print("\n✅ Validation passed with warnings")
            print("🚀 Safe to deploy, but review warnings")
        else:
            print("\n❌ Validation failed")
            print("🔧 Fix errors before deployment")
            
        self.generate_deployment_commands()
        
        return len(self.errors) == 0

def main():
    """Main execution function"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("Usage: python validate-deployment.py")
            print("Validates deployment configuration for Koyeb, Vercel, and Netlify")
            return
            
    validator = DeploymentValidator()
    success = validator.run_validation()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
