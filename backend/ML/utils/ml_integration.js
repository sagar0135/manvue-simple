/**
 * MANVUE ML Integration Utilities
 * Connects the frontend with the ML API for product categorization
 */

class MANVUEMLIntegration {
    constructor(apiBaseUrl = 'http://localhost:5000') {
        this.apiBaseUrl = apiBaseUrl;
        this.isOnline = false;
        this.fallbackEnabled = true;
        this.checkAPIStatus();
    }

    async checkAPIStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            this.isOnline = data.status === 'healthy';
            console.log('ML API Status:', this.isOnline ? 'Online' : 'Offline');
        } catch (error) {
            this.isOnline = false;
            console.warn('ML API not available, using fallback mode');
        }
    }

    async analyzeImage(imageData) {
        if (this.isOnline) {
            return await this.callMLAPI(imageData);
        } else if (this.fallbackEnabled) {
            return this.fallbackAnalysis(imageData);
        } else {
            throw new Error('ML API unavailable and fallback disabled');
        }
    }

    async callMLAPI(imageData) {
        try {
            showMessage('🤖 Analyzing image with FastAPI ML...');
            
            const response = await fetch(`${this.apiBaseUrl}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: imageData,
                    include_colors: true
                })
            });

            if (!response.ok) {
                const errorDetail = await response.text();
                throw new Error(`FastAPI request failed: ${response.status} - ${errorDetail}`);
            }

            const result = await response.json();
            
            // FastAPI returns structured response with success field
            if (result.success !== false) {
                return this.formatMLResponse(result);
            } else {
                throw new Error(result.detail || 'FastAPI ML prediction failed');
            }
        } catch (error) {
            console.error('FastAPI ML Error:', error);
            
            if (this.fallbackEnabled) {
                console.log('Falling back to simulated analysis');
                return this.fallbackAnalysis(imageData);
            } else {
                throw error;
            }
        }
    }

    formatMLResponse(mlResult) {
        return {
            detectedItems: mlResult.detected_items.map(item => ({
                name: item.name,
                category: item.category,
                confidence: item.confidence
            })),
            colors: mlResult.colors || [],
            similarProducts: this.findSimilarProductsFromML(mlResult.detected_items),
            confidence: mlResult.overall_confidence,
            processingTime: mlResult.processing_time,
            source: 'fastapi_ml',
            modelVersion: mlResult.model_version,
            timestamp: mlResult.timestamp
        };
    }

    findSimilarProductsFromML(detectedItems) {
        const similarProducts = [];
        
        detectedItems.forEach(item => {
            // Find products matching the ML detected category
            const matchingProducts = products.filter(product => {
                return product.type === item.type || 
                       product.category === item.category ||
                       product.name.toLowerCase().includes(item.name.toLowerCase()) ||
                       product.tags.some(tag => tag.toLowerCase().includes(item.name.toLowerCase()));
            });
            
            matchingProducts.slice(0, 2).forEach(product => {
                if (!similarProducts.find(p => p.id === product.id)) {
                    similarProducts.push({
                        ...product,
                        matchScore: Math.min(95, Math.floor(item.confidence + (item.confidence_boost * 100)))
                    });
                }
            });
        });
        
        return similarProducts.slice(0, 6);
    }

    fallbackAnalysis(imageData) {
        // Fallback to the existing simulation when ML API is unavailable
        console.log('Using fallback image analysis');
        
        const detectedItems = this.generateFallbackDetection();
        const colors = this.generateFallbackColors();
        const similarProducts = this.findSimilarProducts(detectedItems);
        
        return {
            detectedItems,
            colors,
            similarProducts,
            confidence: Math.floor(Math.random() * 15) + 85,
            processingTime: (Math.random() * 1.5 + 0.3).toFixed(1) + 's',
            source: 'fallback'
        };
    }

    generateFallbackDetection() {
        const possibleItems = [
            { name: 'Dress Shirt', category: 'tops', confidence: 92 },
            { name: 'Casual T-Shirt', category: 'tops', confidence: 88 },
            { name: 'Denim Jeans', category: 'bottoms', confidence: 95 },
            { name: 'Chino Pants', category: 'bottoms', confidence: 87 },
            { name: 'Sneakers', category: 'shoes', confidence: 91 },
            { name: 'Dress Shoes', category: 'shoes', confidence: 89 },
            { name: 'Blazer', category: 'outerwear', confidence: 93 },
            { name: 'Polo Shirt', category: 'tops', confidence: 86 }
        ];
        
        const numItems = Math.floor(Math.random() * 3) + 2;
        const selectedItems = [];
        
        for (let i = 0; i < numItems; i++) {
            const randomItem = possibleItems[Math.floor(Math.random() * possibleItems.length)];
            if (!selectedItems.find(item => item.name === randomItem.name)) {
                selectedItems.push(randomItem);
            }
        }
        
        return selectedItems.sort((a, b) => b.confidence - a.confidence);
    }

    generateFallbackColors() {
        const detectedColors = [
            { hex: '#1a1a1a', name: 'Charcoal', dominance: 0.35 },
            { hex: '#4169E1', name: 'Royal Blue', dominance: 0.25 },
            { hex: '#FFFFFF', name: 'White', dominance: 0.20 },
            { hex: '#2F4F4F', name: 'Dark Slate', dominance: 0.15 },
            { hex: '#C0C0C0', name: 'Silver', dominance: 0.05 }
        ];
        
        const numColors = Math.floor(Math.random() * 3) + 3;
        return detectedColors.slice(0, numColors);
    }

    findSimilarProducts(detectedItems) {
        const similarProducts = [];
        
        detectedItems.forEach(item => {
            const matchingProducts = products.filter(product => {
                return product.name.toLowerCase().includes(item.name.toLowerCase()) ||
                       product.tags.some(tag => tag.toLowerCase().includes(item.name.toLowerCase()));
            });
            
            matchingProducts.slice(0, 2).forEach(product => {
                if (!similarProducts.find(p => p.id === product.id)) {
                    similarProducts.push({
                        ...product,
                        matchScore: Math.floor(Math.random() * 20) + 80
                    });
                }
            });
        });
        
        return similarProducts.slice(0, 6);
    }

    async getCategories() {
        try {
            if (this.isOnline) {
                const response = await fetch(`${this.apiBaseUrl}/categories`);
                const data = await response.json();
                return data.categories;
            } else {
                return this.getFallbackCategories();
            }
        } catch (error) {
            console.error('Error getting categories:', error);
            return this.getFallbackCategories();
        }
    }

    getFallbackCategories() {
        return {
            'T-Shirt': { category: 'tops', type: 'tops', confidence_boost: 0.15 },
            'Shirt': { category: 'tops', type: 'tops', confidence_boost: 0.18 },
            'Trouser': { category: 'bottoms', type: 'bottoms', confidence_boost: 0.16 },
            'Sneaker': { category: 'shoes', type: 'shoes', confidence_boost: 0.18 },
            'Coat': { category: 'outerwear', type: 'outerwear', confidence_boost: 0.20 }
        };
    }

    async retrainModel(newData) {
        if (!this.isOnline) {
            throw new Error('ML API unavailable for retraining');
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/retrain`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    training_data: newData
                })
            });

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Retraining error:', error);
            throw error;
        }
    }

    // Integration with existing MANVUE functions
    integrateWithVisualSearch() {
        // Override the existing performImageAnalysis function
        window.performImageAnalysisML = async (imageData) => {
            try {
                const results = await this.analyzeImage(imageData);
                return results;
            } catch (error) {
                console.error('ML Integration Error:', error);
                // Fallback to original analysis
                return window.performImageAnalysis(imageData);
            }
        };
    }
}

// Create global ML integration instance
const manvueML = new MANVUEMLIntegration();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MANVUEMLIntegration;
}

// Auto-integrate when loaded
document.addEventListener('DOMContentLoaded', () => {
    manvueML.integrateWithVisualSearch();
    console.log('MANVUE ML Integration loaded');
});
