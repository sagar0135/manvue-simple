#!/usr/bin/env python3
"""
MANVUE Image Setup Script
Complete setup for converting images to GridFS and seeding products
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.database import test_connection, list_images
from convert_images_to_gridfs import convert_all_product_images
from seed_product_data import seed_products

class MANVUEImageSetup:
    def __init__(self):
        self.setup_complete = False
        self.images_converted = False
        self.products_seeded = False

    async def check_database_connection(self):
        """Check if MongoDB is accessible"""
        print("🔌 Checking database connection...")
        
        if await test_connection():
            print("✅ Database connection successful!")
            return True
        else:
            print("❌ Database connection failed!")
            print("   Please check your MongoDB setup:")
            print("   1. Ensure MongoDB is running")
            print("   2. Check your MONGO_URI environment variable")
            print("   3. Verify network connectivity")
            return False

    async def check_existing_images(self):
        """Check if we already have images in GridFS"""
        print("📁 Checking existing images in GridFS...")
        
        try:
            images = await list_images(limit=10)
            if images:
                print(f"✅ Found {len(images)} existing images in GridFS")
                for img in images[:5]:  # Show first 5
                    print(f"   - {img['filename']} ({img['content_type']})")
                if len(images) > 5:
                    print(f"   ... and {len(images) - 5} more")
                return True
            else:
                print("📭 No existing images found in GridFS")
                return False
        except Exception as e:
            print(f"⚠️  Error checking existing images: {e}")
            return False

    async def convert_images(self):
        """Convert external images to GridFS"""
        print("\n🔄 Converting external images to GridFS...")
        
        try:
            converted_products = await convert_all_product_images()
            if converted_products:
                print("✅ Image conversion completed successfully!")
                self.images_converted = True
                return True
            else:
                print("❌ Image conversion failed!")
                return False
        except Exception as e:
            print(f"❌ Error during image conversion: {e}")
            return False

    async def seed_database(self):
        """Seed database with product data"""
        print("\n🌱 Seeding database with product data...")
        
        try:
            await seed_products()
            print("✅ Database seeding completed successfully!")
            self.products_seeded = True
            return True
        except Exception as e:
            print(f"❌ Error during database seeding: {e}")
            return False

    async def verify_setup(self):
        """Verify the complete setup"""
        print("\n🔍 Verifying setup...")
        
        # Check if we have images in GridFS
        has_images = await self.check_existing_images()
        
        # Check if converted products file exists
        converted_file = "converted_products_with_gridfs_ids.json"
        has_converted_file = os.path.exists(converted_file)
        
        if has_images and has_converted_file:
            print("✅ Setup verification successful!")
            print("   - Images are stored in GridFS")
            print("   - Product data includes GridFS image IDs")
            print("   - API can serve images from GridFS")
            return True
        else:
            print("⚠️  Setup verification found issues:")
            if not has_images:
                print("   - No images found in GridFS")
            if not has_converted_file:
                print("   - No converted products file found")
            return False

    def print_next_steps(self):
        """Print instructions for next steps"""
        print("\n📝 Next Steps:")
        print("1. Start your API server:")
        print("   python api/start_enhanced_backend.py")
        print()
        print("2. Test image serving (replace {file_id} with actual ID):")
        print("   curl http://localhost:5001/api/images/{file_id}")
        print()
        print("3. Test product API:")
        print("   curl http://localhost:5001/api/products")
        print()
        print("4. Update your frontend PRODUCT_ID to use one of the created products")
        print()
        print("5. Open your product page to see GridFS images!")

    async def run_complete_setup(self):
        """Run the complete MANVUE image setup process"""
        print("🚀 MANVUE Image Setup - Converting External Images to GridFS")
        print("=" * 60)
        
        # Step 1: Check database connection
        if not await self.check_database_connection():
            print("\n❌ Setup failed: Database connection issue")
            return False
        
        # Step 2: Check existing setup
        has_existing_images = await self.check_existing_images()
        
        # Step 3: Convert images if needed
        if not has_existing_images:
            print("\n🎯 No existing images found. Starting conversion process...")
            if not await self.convert_images():
                print("\n❌ Setup failed: Image conversion issue")
                return False
        else:
            print("\n💡 Images already exist. Skipping conversion.")
            self.images_converted = True
        
        # Step 4: Seed database
        print("\n🎯 Starting database seeding...")
        if not await self.seed_database():
            print("\n❌ Setup failed: Database seeding issue")
            return False
        
        # Step 5: Verify setup
        if not await self.verify_setup():
            print("\n⚠️  Setup completed with warnings")
        else:
            print("\n🎉 Setup completed successfully!")
            self.setup_complete = True
        
        # Step 6: Print next steps
        self.print_next_steps()
        
        return self.setup_complete

async def main():
    """Main setup function"""
    setup = MANVUEImageSetup()
    success = await setup.run_complete_setup()
    
    if success:
        print("\n✨ MANVUE image setup completed successfully!")
        print("   Your images are now stored in MongoDB GridFS.")
        print("   Products are seeded with GridFS image references.")
        print("   Your API can serve images directly from the database.")
    else:
        print("\n💥 Setup encountered issues. Please check the output above.")
        print("   You may need to:")
        print("   - Fix MongoDB connection issues")
        print("   - Check network connectivity for image downloads")
        print("   - Verify your environment setup")

if __name__ == "__main__":
    asyncio.run(main())
