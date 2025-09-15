#!/usr/bin/env python3
"""
Local Image Processor Usage Example
Demonstrates how to use the LocalImageProcessor service for dataset integration
"""

import sys
import os
import pandas as pd
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

def create_sample_dataframe():
    """
    Create a sample DataFrame for testing purposes
    """
    sample_data = {
        'image': [
            'product1.jpg',
            'product2.jpg', 
            'product3.jpg',
            'product4.jpg',
            'product5.jpg'
        ],
        'display name': [
            'Sample T-Shirt 1',
            'Sample Jeans 1',
            'Sample Jacket 1',
            'Sample Shoes 1',
            'Sample Hat 1'
        ],
        'description': [
            'Comfortable cotton t-shirt',
            'Classic blue jeans',
            'Warm winter jacket',
            'Comfortable running shoes',
            'Stylish baseball cap'
        ],
        'category': [
            'tshirts',
            'bottoms',
            'jackets',
            'shoes',
            'accessories'
        ]
    }
    
    return pd.DataFrame(sample_data)

def main():
    """
    Main function demonstrating LocalImageProcessor usage
    """
    print("🚀 Local Image Processor Example")
    print("=" * 50)
    
    # Create sample data
    print("\n📊 Creating sample DataFrame...")
    df = create_sample_dataframe()
    print(f"Created DataFrame with {len(df)} products")
    print(df.head())
    
    # Initialize processor
    print("\n🔧 Initializing LocalImageProcessor...")
    processor = LocalImageProcessor(
        local_base_url="http://127.0.0.1:5500",
        images_folder="frontend/images"
    )
    
    # Example 1: Process images directly from source
    print("\n📁 Example 1: Processing images directly from source...")
    print("Note: This example assumes you have a source image directory")
    
    # Uncomment and modify these lines for your actual setup:
    # SOURCE_IMAGE_DIR = "/path/to/your/dataset/images"
    # docs = processor.process_local_images_directly(df, SOURCE_IMAGE_DIR, num_samples=3)
    # print(f"Processed {len(docs)} images directly")
    
    # Example 2: Copy images to website folder
    print("\n📁 Example 2: Copying images to website folder...")
    print("Note: This example assumes you have a source image directory")
    
    # Uncomment and modify these lines for your actual setup:
    # SOURCE_IMAGE_DIR = "/path/to/your/dataset/images"
    # products = processor.copy_dataset_images_to_website(df, SOURCE_IMAGE_DIR, num_samples=3)
    # print(f"Copied {len(products)} images to website folder")
    
    # Example 3: Complete setup
    print("\n📁 Example 3: Complete setup...")
    print("Note: This example assumes you have a source image directory")
    
    # Uncomment and modify these lines for your actual setup:
    # SOURCE_IMAGE_DIR = "/path/to/your/dataset/images"
    # docs = processor.setup_local_website_images(df, SOURCE_IMAGE_DIR, num_samples=3)
    # print(f"Complete setup processed {len(docs)} images")
    
    # Example 4: Image validation
    print("\n🔍 Example 4: Image validation...")
    print("This example shows how to validate images")
    
    # Create a test image path (you would use actual paths)
    test_image_path = "frontend/images/test.jpg"
    
    if os.path.exists(test_image_path):
        is_valid = processor.validate_image(test_image_path)
        print(f"Image {test_image_path} is valid: {is_valid}")
        
        if is_valid:
            image_info = processor.get_image_info(test_image_path)
            print(f"Image info: {image_info}")
    else:
        print(f"Test image not found at {test_image_path}")
    
    print("\n✅ Example completed!")
    print("\n💡 Next steps:")
    print("1. Update SOURCE_IMAGE_DIR to point to your actual dataset images")
    print("2. Uncomment the example code sections above")
    print("3. Run the script to process your images")
    print("4. Start your local server: python -m http.server 5500")
    print("5. Visit http://127.0.0.1:5500 to see your processed images")

def process_real_dataset(csv_path: str, image_dir: str, num_samples: int = 10):
    """
    Process a real dataset from CSV file
    
    Args:
        csv_path: Path to CSV file containing product data
        image_dir: Directory containing product images
        num_samples: Number of samples to process
    """
    try:
        # Load CSV data
        print(f"📊 Loading dataset from: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} products from CSV")
        
        # Initialize processor
        processor = LocalImageProcessor()
        
        # Process images
        print(f"🔄 Processing {num_samples} images...")
        docs = processor.setup_local_website_images(df, image_dir, num_samples)
        
        print(f"✅ Successfully processed {len(docs)} images")
        
        # Save results
        results_df = pd.DataFrame(docs)
        output_path = "processed_images_results.csv"
        results_df.to_csv(output_path, index=False)
        print(f"💾 Results saved to: {output_path}")
        
        return docs
        
    except Exception as e:
        logger.error(f"Error processing dataset: {e}")
        return None

if __name__ == "__main__":
    # Run the main example
    main()
    
    # Uncomment to process a real dataset:
    # process_real_dataset(
    #     csv_path="your_dataset.csv",
    #     image_dir="/path/to/your/images",
    #     num_samples=10
    # )
