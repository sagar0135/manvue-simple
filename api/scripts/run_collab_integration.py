"""
Script to run collab system integration
This script executes the collab functionality and generates the required files for the API
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_collab_system():
    """Run the collab system to generate embeddings and FAISS index"""
    try:
        # Path to the collab script
        collab_script = project_root / "collab" / "Untitled-2.py"
        
        if not collab_script.exists():
            logger.error(f"Collab script not found at {collab_script}")
            return False
        
        logger.info("🚀 Running collab system to generate embeddings and FAISS index...")
        
        # Change to the collab directory
        os.chdir(collab_script.parent)
        
        # Run the collab script
        result = subprocess.run([
            sys.executable, 
            str(collab_script)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ Collab system executed successfully!")
            logger.info("📊 Generated files:")
            
            # Check for generated files
            generated_files = [
                "fashion.index",
                "metadata.json"
            ]
            
            for file_name in generated_files:
                if os.path.exists(file_name):
                    logger.info(f"  ✅ {file_name}")
                    # Copy to API directory
                    import shutil
                    api_dir = project_root / "api"
                    shutil.copy2(file_name, api_dir)
                    logger.info(f"  📁 Copied {file_name} to API directory")
                else:
                    logger.warning(f"  ⚠️ {file_name} not found")
            
            return True
        else:
            logger.error(f"❌ Collab system failed with return code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error running collab system: {e}")
        return False

def setup_environment():
    """Set up the Python environment with required dependencies"""
    logger.info("📦 Setting up environment...")
    
    # Install required packages
    packages = [
        "transformers",
        "torch",
        "torchvision", 
        "faiss-cpu",
        "datasets",
        "scikit-learn",
        "xgboost",
        "lightgbm",
        "matplotlib",
        "seaborn",
        "umap-learn",
        "pillow",
        "pymongo",
        "gridfs"
    ]
    
    for package in packages:
        try:
            logger.info(f"Installing {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True, capture_output=True)
            logger.info(f"✅ {package} installed")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install {package}: {e}")

def verify_integration():
    """Verify that the integration files are available"""
    logger.info("🔍 Verifying integration...")
    
    api_dir = project_root / "api"
    required_files = [
        api_dir / "fashion.index",
        api_dir / "metadata.json"
    ]
    
    all_good = True
    for file_path in required_files:
        if file_path.exists():
            logger.info(f"✅ {file_path.name} found")
        else:
            logger.error(f"❌ {file_path.name} missing")
            all_good = False
    
    if all_good:
        logger.info("🎉 Integration verification successful!")
    else:
        logger.error("⚠️ Some integration files are missing")
    
    return all_good

def main():
    """Main integration process"""
    logger.info("🔗 Starting MANVUE Collab Integration Process")
    logger.info("=" * 50)
    
    # Step 1: Setup environment
    setup_environment()
    
    # Step 2: Run collab system
    if run_collab_system():
        # Step 3: Verify integration
        if verify_integration():
            logger.info("🎉 Integration completed successfully!")
            logger.info("\n📋 Next steps:")
            logger.info("1. Start your API server")
            logger.info("2. Test the visual search endpoints")
            logger.info("3. Integrate with your frontend")
        else:
            logger.error("❌ Integration verification failed")
    else:
        logger.error("❌ Collab system execution failed")

if __name__ == "__main__":
    main()

