// Main Products Data File
import tshirts from './tshirts.js';
import shirts from './shirts.js';
import bottoms from './bottoms.js';
import jackets from './jackets.js';
import accessories from './accessories.js';

// Combine all product categories
const allProducts = [
    ...tshirts,
    ...shirts,
    ...bottoms,
    ...jackets,
    ...accessories
];

// Product categories for easy filtering
const productCategories = {
    tshirts: tshirts,
    shirts: shirts,
    bottoms: bottoms,
    jackets: jackets,
    accessories: accessories
};

// Helper functions for product management
const productUtils = {
    // Get all products
    getAllProducts: () => allProducts,
    
    // Get products by category
    getByCategory: (category) => {
        switch(category.toLowerCase()) {
            case 'tshirts':
            case 't-shirts':
                return tshirts;
            case 'shirts':
                return shirts;
            case 'bottoms':
                return bottoms;
            case 'jackets':
            case 'outerwear':
                return jackets;
            case 'accessories':
                return accessories;
            default:
                return allProducts;
        }
    },
    
    // Get products by type
    getByType: (type) => {
        return allProducts.filter(product => 
            product.type.toLowerCase().includes(type.toLowerCase()) ||
            product.category.toLowerCase().includes(type.toLowerCase())
        );
    },
    
    // Search products
    searchProducts: (query) => {
        const searchTerm = query.toLowerCase();
        return allProducts.filter(product =>
            product.name.toLowerCase().includes(searchTerm) ||
            product.description.toLowerCase().includes(searchTerm) ||
            product.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
            product.brand.toLowerCase().includes(searchTerm)
        );
    },
    
    // Filter by price range
    filterByPrice: (minPrice, maxPrice) => {
        return allProducts.filter(product =>
            product.price >= minPrice && product.price <= maxPrice
        );
    },
    
    // Filter by brand
    filterByBrand: (brand) => {
        return allProducts.filter(product =>
            product.brand.toLowerCase().includes(brand.toLowerCase())
        );
    },
    
    // Get trending products (highest rated with good review count)
    getTrendingProducts: (limit = 10) => {
        return allProducts
            .filter(product => product.rating >= 4.0 && product.reviews >= 100)
            .sort((a, b) => (b.rating * Math.log(b.reviews)) - (a.rating * Math.log(a.reviews)))
            .slice(0, limit);
    },
    
    // Get new arrivals (products with newest tag or high ratings)
    getNewArrivals: (limit = 12) => {
        return allProducts
            .sort((a, b) => b.rating - a.rating)
            .slice(0, limit);
    },
    
    // Get products on sale
    getDealsProducts: (limit = 8) => {
        return allProducts
            .filter(product => product.discount > 0)
            .sort((a, b) => b.discount - a.discount)
            .slice(0, limit);
    }
};

// Export everything
export {
    allProducts,
    productCategories,
    productUtils,
    tshirts,
    shirts,
    bottoms,
    jackets,
    accessories
};

export default {
    allProducts,
    productCategories,
    productUtils
};
