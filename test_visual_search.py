#!/usr/bin/env python3
"""
Test script for the visual search functionality
"""

import asyncio
import json
import base64
import requests
from PIL import Image
import io

# Test configuration
API_BASE_URL = "http://localhost:5000"
TEST_IMAGE_URL = "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&auto=format"

async def test_visual_search():
    """Test the visual search API"""
    
    print("🧪 Testing Visual Search API")
    print("=" * 50)
    
    try:
        # 1. Test health check
        print("1. Testing health check...")
        response = requests.get(f"{API_BASE_URL}/visual-search/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
        
        # 2. Download test image
        print("\n2. Downloading test image...")
        image_response = requests.get(TEST_IMAGE_URL)
        if image_response.status_code == 200:
            # Convert to base64
            image_data = base64.b64encode(image_response.content).decode('utf-8')
            image_data_url = f"data:image/jpeg;base64,{image_data}"
            print("✅ Test image downloaded and encoded")
        else:
            print(f"❌ Failed to download test image: {image_response.status_code}")
            return
        
        # 3. Test visual search
        print("\n3. Testing visual search...")
        search_request = {
            "image": image_data_url,
            "max_products": 5,
            "max_outfits": 2
        }
        
        response = requests.post(
            f"{API_BASE_URL}/visual-search/search",
            json=search_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Visual search successful")
            print(f"   Found {len(result.get('similar_products', []))} similar products")
            print(f"   Generated {len(result.get('outfit_recommendations', []))} outfit recommendations")
            
            # Display results
            if result.get('similar_products'):
                print("\n   Similar Products:")
                for i, product in enumerate(result['similar_products'][:3], 1):
                    print(f"   {i}. {product['product']['name']} - {product['confidence']}% confidence")
            
            if result.get('outfit_recommendations'):
                print("\n   Outfit Recommendations:")
                for i, outfit in enumerate(result['outfit_recommendations'], 1):
                    print(f"   {i}. {outfit['style_description']} - {outfit['confidence']}% match")
                    print(f"      Items: {len(outfit['items'])} - Total: £{outfit['total_price']:.2f}")
            
            if result.get('analysis_metadata'):
                metadata = result['analysis_metadata']
                print(f"\n   Processing time: {metadata.get('processing_time', 'N/A')}")
                print(f"   CLIP model available: {metadata.get('clip_model_available', False)}")
        
        else:
            print(f"❌ Visual search failed: {response.status_code}")
            print(f"   Error: {response.text}")
        
        # 4. Test complete image analysis
        print("\n4. Testing complete image analysis...")
        analysis_request = {
            "image": image_data_url,
            "include_colors": True,
            "include_outfit_suggestions": True
        }
        
        response = requests.post(
            f"{API_BASE_URL}/visual-search/analyze",
            json=analysis_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Image analysis successful")
            print(f"   Overall confidence: {result.get('overall_confidence', 0)}%")
            print(f"   Processing time: {result.get('processing_time', 'N/A')}")
        else:
            print(f"❌ Image analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
        
        # 5. Test compatible categories
        print("\n5. Testing compatible categories...")
        response = requests.get(f"{API_BASE_URL}/visual-search/categories")
        if response.status_code == 200:
            result = response.json()
            print("✅ Compatible categories retrieved")
            print(f"   Available outfit rules: {len(result.get('outfit_rules', {}))}")
        else:
            print(f"❌ Failed to get compatible categories: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 Visual Search API Test Complete!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

def test_frontend_integration():
    """Test frontend integration"""
    print("\n🌐 Testing Frontend Integration")
    print("=" * 50)
    
    try:
        # Test if frontend is accessible
        response = requests.get("http://localhost:8002")
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
        
        # Test if visual search modal exists in HTML
        if "visual-search-modal" in response.text:
            print("✅ Visual search modal found in frontend")
        else:
            print("❌ Visual search modal not found in frontend")
        
        if "performVisualSearch" in response.text:
            print("✅ Visual search JavaScript function found")
        else:
            print("❌ Visual search JavaScript function not found")
            
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")

if __name__ == "__main__":
    print("🚀 MANVUE Visual Search Test Suite")
    print("=" * 50)
    print("This script tests the complete visual search functionality")
    print("Make sure the API server is running on http://localhost:5000")
    print("Make sure the frontend is running on http://localhost:8002")
    print()
    
    # Run async tests
    asyncio.run(test_visual_search())
    
    # Run frontend tests
    test_frontend_integration()
    
    print("\n📋 Test Summary:")
    print("- Visual Search API endpoints")
    print("- Image processing and similarity search")
    print("- Outfit recommendation generation")
    print("- Frontend integration")
    print("\n✨ If all tests pass, your visual search feature is ready!")
