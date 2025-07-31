#!/usr/bin/env python3
"""
Multi-platform deployment script for Cookware Analyzer
Supports both Koyeb and Vercel deployments
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class CookwareDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.required_files = ["app.py", "requirements.txt", "koyeb.yaml", "vercel.json"]
        
    def check_command_exists(self, command):
        """Check if a command exists in PATH"""
        return shutil.which(command) is not None
    
    def run_command(self, command, shell=False):
        """Run a command and return success status"""
        try:
            result = subprocess.run(command, shell=shell, check=True, 
                                  capture_output=True, text=True)
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def pre_deployment_checks(self):
        """Run pre-deployment validation checks"""
        print("🔍 Running pre-deployment checks...")
        
        # Check required files
        for file in self.required_files:
            file_path = self.project_root / file
            if not file_path.exists():
                print(f"❌ Required file missing: {file}")
                return False
        
        # Check models directory
        models_dir = self.project_root / "models"
        if not models_dir.exists():
            print("❌ Models directory not found!")
            return False
        
        # Check for model files
        keras_files = list(models_dir.glob("*.keras"))
        if not keras_files:
            print("❌ No .keras model files found in models directory!")
            return False
        
        print("✅ All pre-deployment checks passed!")
        return True
    
    def deploy_koyeb(self):
        """Deploy to Koyeb"""
        print("🚀 Deploying to Koyeb...")
        
        if not self.check_command_exists("koyeb"):
            print("❌ Koyeb CLI not found. Please install it first:")
            print("   Visit: https://www.koyeb.com/docs/cli/installation")
            return False
        
        print("📦 Deploying with Koyeb configuration...")
        success = self.run_command(["koyeb", "app", "deploy", "cookware-analyzer", 
                                   "--config", "koyeb.yaml"])
        
        if success:
            print("✅ Koyeb deployment initiated!")
            print("🔗 Check status: https://app.koyeb.com/")
        
        return success
    
    def deploy_vercel(self):
        """Deploy to Vercel"""
        print("🚀 Deploying to Vercel...")
        
        # Check Node.js first
        if not self.check_command_exists("node"):
            print("❌ Node.js not found. Please install Node.js first:")
            print("   Visit: https://nodejs.org/")
            return False
        
        # Install Vercel CLI if not available
        if not self.check_command_exists("vercel"):
            print("📦 Installing Vercel CLI...")
            success = self.run_command(["npm", "i", "-g", "vercel"])
            if not success:
                print("❌ Failed to install Vercel CLI")
                return False
        
        print("📦 Deploying with Vercel configuration...")
        
        # Backup original requirements.txt
        original_req = self.project_root / "requirements.txt"
        vercel_req = self.project_root / "requirements-vercel.txt"
        backup_req = self.project_root / "requirements.txt.backup"
        
        try:
            # Backup and switch to Vercel requirements
            if original_req.exists():
                shutil.copy2(original_req, backup_req)
            shutil.copy2(vercel_req, original_req)
            
            # Deploy to Vercel
            success = self.run_command(["vercel", "deploy", "--prod"])
            
            # Restore original requirements
            if backup_req.exists():
                shutil.copy2(backup_req, original_req)
                backup_req.unlink()
            
            if success:
                print("✅ Vercel deployment completed!")
                print("🔗 Your app is now live on Vercel")
            
            return success
            
        except Exception as e:
            print(f"❌ Error during Vercel deployment: {e}")
            # Restore backup if exists
            if backup_req.exists():
                shutil.copy2(backup_req, original_req)
                backup_req.unlink()
            return False
    
    def deploy_both(self):
        """Deploy to both platforms"""
        print("🚀 Deploying to both Koyeb and Vercel...")
        
        koyeb_success = self.deploy_koyeb()
        print()
        vercel_success = self.deploy_vercel()
        
        if koyeb_success and vercel_success:
            print("\n🎉 Deployment to both platforms completed successfully!")
        elif koyeb_success:
            print("\n⚠️ Koyeb deployment successful, Vercel deployment failed")
        elif vercel_success:
            print("\n⚠️ Vercel deployment successful, Koyeb deployment failed")
        else:
            print("\n❌ Both deployments failed")
        
        return koyeb_success or vercel_success
    
    def show_menu(self):
        """Show interactive menu"""
        print("\n📋 Deployment Options:")
        print("1. Deploy to Koyeb only")
        print("2. Deploy to Vercel only")
        print("3. Deploy to both platforms")
        print("4. Run pre-deployment checks only")
        print("5. Exit")
        print()
    
    def run(self, args=None):
        """Main execution function"""
        print("🍳 Cookware Analyzer - Multi-Platform Deployment Script")
        print("=======================================================")
        
        # Run pre-deployment checks
        if not self.pre_deployment_checks():
            return False
        
        # Handle command line arguments
        if args:
            if args[0] == "koyeb":
                return self.deploy_koyeb()
            elif args[0] == "vercel":
                return self.deploy_vercel()
            elif args[0] == "both":
                return self.deploy_both()
            elif args[0] == "check":
                print("✅ Pre-deployment checks completed successfully!")
                return True
            else:
                print(f"❌ Invalid argument: {args[0]}")
                print("Valid arguments: koyeb, vercel, both, check")
                return False
        
        # Interactive mode
        while True:
            self.show_menu()
            try:
                choice = input("Select an option (1-5): ").strip()
                
                if choice == "1":
                    self.deploy_koyeb()
                    break
                elif choice == "2":
                    self.deploy_vercel()
                    break
                elif choice == "3":
                    self.deploy_both()
                    break
                elif choice == "4":
                    print("✅ Pre-deployment checks completed successfully!")
                elif choice == "5":
                    print("👋 Goodbye!")
                    return True
                else:
                    print("❌ Invalid option. Please select 1-5.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return True

if __name__ == "__main__":
    deployer = CookwareDeployer()
    args = sys.argv[1:] if len(sys.argv) > 1 else None
    success = deployer.run(args)
    sys.exit(0 if success else 1)
