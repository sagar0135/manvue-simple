#!/usr/bin/env python3
"""
ManVue API Test Script
Quick testing of all API endpoints
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:5000"

def test_api_health():
    """Test API health endpoint"""
    print("🔍 Testing API Health...")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy: {data.get('message', 'OK')}")
            print(f"📋 Version: {data.get('version', 'Unknown')}")
            print(f"🚀 Features: {', '.join(data.get('features', []))}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API not responding: {e}")
        return False

def test_get_products():
    """Test getting all products"""
    print("\n📦 Testing Get Products...")
    try:
        response = requests.get(f"{API_BASE_URL}/products", timeout=5)
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Found {len(products)} products")
            if products:
                print(f"📋 Sample product: {products[0].get('title', 'Unknown')}")
            return True
        else:
            print(f"❌ Get products failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Get products error: {e}")
        return False

def test_text_search():
    """Test AI text search"""
    print("\n🔍 Testing AI Text Search...")
    try:
        search_data = {
            "query": "cotton shirt",
            "category": "tops"
        }
        response = requests.post(
            f"{API_BASE_URL}/products/search",
            json=search_data,
            timeout=10
        )
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Search successful: {results.get('total', 0)} results")
            if results.get('results'):
                print(f"📋 Top result: {results['results'][0].get('title', 'Unknown')}")
            return True
        else:
            print(f"❌ Text search failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Text search error: {e}")
        return False

def test_image_search():
    """Test AI image search"""
    print("\n📸 Testing AI Image Search...")
    try:
        # Use a sample base64 image (1x1 pixel)
        sample_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        
        search_data = {
            "image": sample_image,
            "include_similar": True
        }
        response = requests.post(
            f"{API_BASE_URL}/products/image-search",
            json=search_data,
            timeout=10
        )
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Image search successful: {results.get('source', 'unknown')}")
            if results.get('similar_products'):
                print(f"📋 Found {len(results['similar_products'])} similar products")
            return True
        else:
            print(f"❌ Image search failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Image search error: {e}")
        return False

def test_add_product():
    """Test adding a new product"""
    print("\n➕ Testing Add Product...")
    try:
        product_data = {
            "title": "Test Product",
            "price": 19.99,
            "category": "tops",
            "type": "test",
            "image_url": "https://via.placeholder.com/150",
            "description": "Test product for API testing",
            "brand": "Test Brand",
            "rating": 4.5
        }
        response = requests.post(
            f"{API_BASE_URL}/products",
            json=product_data,
            timeout=5
        )
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product added: {product.get('title', 'Unknown')} (ID: {product.get('id', 'Unknown')})")
            return product.get('id')
        else:
            print(f"❌ Add product failed: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Add product error: {e}")
        return None

def test_delete_product(product_id):
    """Test deleting a product"""
    if not product_id:
        print("\n🗑️ Skipping delete test (no product ID)")
        return False
        
    print(f"\n🗑️ Testing Delete Product (ID: {product_id})...")
    try:
        response = requests.delete(f"{API_BASE_URL}/products/{product_id}", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Product deleted: {result.get('message', 'OK')}")
            return True
        else:
            print(f"❌ Delete product failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Delete product error: {e}")
        return False

def test_ml_health():
    """Test ML service health"""
    print("\n🧠 Testing ML Service Health...")
    try:
        response = requests.get(f"{API_BASE_URL}/ml/health", timeout=5)
        if response.status_code == 200:
            ml_status = response.json()
            print(f"✅ ML service: {ml_status.get('ml_service', 'unknown')}")
            return True
        else:
            print(f"❌ ML health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ ML health check error: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("🧪 MANVUE API TEST SUITE")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: API Health
    total_tests += 1
    if test_api_health():
        tests_passed += 1
    
    # Test 2: Get Products
    total_tests += 1
    if test_get_products():
        tests_passed += 1
    
    # Test 3: Text Search
    total_tests += 1
    if test_text_search():
        tests_passed += 1
    
    # Test 4: Image Search
    total_tests += 1
    if test_image_search():
        tests_passed += 1
    
    # Test 5: Add Product
    total_tests += 1
    product_id = None
    if test_add_product():
        tests_passed += 1
        # Get the product ID for deletion test
        try:
            response = requests.get(f"{API_BASE_URL}/products", timeout=5)
            if response.status_code == 200:
                products = response.json()
                # Find the test product
                for product in products:
                    if product.get('title') == 'Test Product':
                        product_id = product.get('id')
                        break
        except:
            pass
    
    # Test 6: Delete Product
    total_tests += 1
    if test_delete_product(product_id):
        tests_passed += 1
    
    # Test 7: ML Health
    total_tests += 1
    if test_ml_health():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    if tests_passed == total_tests:
        print("🎉 All tests passed! API is working perfectly.")
    else:
        print("⚠️ Some tests failed. Check the API server.")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()
