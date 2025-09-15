#!/usr/bin/env python3
"""
Convert JavaScript product files to JSON format
"""

import json
import re
import os
from pathlib import Path

def convert_js_to_json(js_content):
    """Convert JavaScript object to JSON format"""
    # Replace single quotes with double quotes
    json_content = js_content.replace("'", '"')
    
    # Fix JavaScript-specific syntax
    json_content = re.sub(r'(\w+):', r'"\1":', json_content)  # Add quotes to keys
    json_content = re.sub(r'(\w+)\s*\(', r'"\1"', json_content)  # Fix function calls
    
    # Remove trailing commas
    json_content = re.sub(r',\s*}', '}', json_content)
    json_content = re.sub(r',\s*]', ']', json_content)
    
    return json_content

def load_products_from_js(file_path):
    """Load products from JavaScript file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find the products array
            start = content.find('const ')
            if start == -1:
                return []
            
            # Find the array start
            array_start = content.find('[', start)
            if array_start == -1:
                return []
            
            # Find the matching closing bracket
            bracket_count = 0
            end = array_start
            for i, char in enumerate(content[array_start:], array_start):
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        end = i + 1
                        break
            
            # Extract the array
            array_content = content[array_start:end]
            
            # Convert to JSON
            json_content = convert_js_to_json(array_content)
            
            # Parse JSON
            products = json.loads(json_content)
            return products
            
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def main():
    """Main function to convert all product files"""
    products = []
    
    # Category files
    category_files = [
        'frontend/data/tshirts.js',
        'frontend/data/shirts.js', 
        'frontend/data/bottoms.js',
        'frontend/data/jackets.js',
        'frontend/data/accessories.js',
        'frontend/data/winter-collection.js'
    ]
    
    for file_path in category_files:
        if os.path.exists(file_path):
            print(f"Loading {file_path}...")
            category_products = load_products_from_js(file_path)
            products.extend(category_products)
            print(f"Loaded {len(category_products)} products from {file_path}")
        else:
            print(f"File not found: {file_path}")
    
    # Save as JSON
    with open('frontend/data/products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2)
    
    print(f"\n✅ Converted {len(products)} products to JSON format")
    print("📁 Saved to: frontend/data/products.json")

if __name__ == "__main__":
    main()
