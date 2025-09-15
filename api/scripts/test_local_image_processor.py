#!/usr/bin/env python3
"""
Test script for LocalImageProcessor integration
"""

import sys
import os
import logging
from pathlib import Path

# Add the parent directory to the path to import services
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.local_image_processor import LocalImageProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_processor_initialization():
    """Test that the processor initializes correctly"""
    print("🧪 Testing processor initialization...")
    
    try:
        processor = LocalImageProcessor()
        print("✅ Processor initialized successfully")
        print(f"   Images folder: {processor.full_images_path}")
        print(f"   Base URL: {processor.local_base_url}")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize processor: {e}")
        return False

def test_directory_creation():
    """Test that the images directory is created"""
    print("\n🧪 Testing directory creation...")
    
    try:
        processor = LocalImageProcessor()
        images_dir = Path(processor.full_images_path)
        
        if images_dir.exists():
            print("✅ Images directory exists")
            print(f"   Path: {images_dir.absolute()}")
            return True
        else:
            print("❌ Images directory was not created")
            return False
    except Exception as e:
        print(f"❌ Error checking directory: {e}")
        return False

def test_image_validation():
    """Test image validation functionality"""
    print("\n🧪 Testing image validation...")
    
    try:
        processor = LocalImageProcessor()
        
        # Test with a non-existent file
        result = processor.validate_image("non_existent_file.jpg")
        if result == False:
            print("✅ Correctly identified non-existent file as invalid")
        else:
            print("❌ Should have identified non-existent file as invalid")
            return False
        
        # Test with a directory (should be invalid)
        result = processor.validate_image(processor.full_images_path)
        if result == False:
            print("✅ Correctly identified directory as invalid image")
        else:
            print("❌ Should have identified directory as invalid image")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error testing image validation: {e}")
        return False

def test_image_info():
    """Test image info functionality"""
    print("\n🧪 Testing image info...")
    
    try:
        processor = LocalImageProcessor()
        
        # Test with a non-existent file
        info = processor.get_image_info("non_existent_file.jpg")
        if info is None:
            print("✅ Correctly returned None for non-existent file")
        else:
            print("❌ Should have returned None for non-existent file")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error testing image info: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Local Image Processor Integration Tests")
    print("=" * 50)
    
    tests = [
        test_processor_initialization,
        test_directory_creation,
        test_image_validation,
        test_image_info
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("📊 Test Results:")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! LocalImageProcessor is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
