"""
ML Voice Integration for ManVue Application

This module integrates voice commands with machine learning models for enhanced
product search and recommendations.
"""

import logging
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import json
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class VoiceMLIntegration:
    """Integrates voice commands with ML models for enhanced functionality"""
    
    def __init__(self, ml_service_url: Optional[str] = None):
        """
        Initialize ML voice integration
        
        Args:
            ml_service_url: URL of the ML service endpoint
        """
        self.ml_service_url = ml_service_url or "http://localhost:8001"
        self.fashion_categories = self._load_fashion_categories()
        self.color_mappings = self._load_color_mappings()
        self.style_keywords = self._load_style_keywords()
        self.user_preferences = {}
        
        logger.info("ML Voice Integration initialized")
    
    def _load_fashion_categories(self) -> Dict[str, List[str]]:
        """Load fashion category mappings for voice recognition"""
        return {
            'tops': ['shirt', 'blouse', 't-shirt', 'tshirt', 'tank top', 'sweater', 'hoodie', 'cardigan'],
            'bottoms': ['pants', 'jeans', 'trousers', 'shorts', 'skirt', 'leggings'],
            'dresses': ['dress', 'gown', 'sundress', 'maxi dress', 'mini dress'],
            'outerwear': ['jacket', 'coat', 'blazer', 'vest', 'windbreaker'],
            'footwear': ['shoes', 'boots', 'sneakers', 'sandals', 'heels', 'flats'],
            'accessories': ['bag', 'purse', 'backpack', 'hat', 'scarf', 'belt', 'jewelry', 'watch']
        }
    
    def _load_color_mappings(self) -> Dict[str, List[str]]:
        """Load color name mappings and variations"""
        return {
            'red': ['red', 'crimson', 'scarlet', 'cherry', 'burgundy', 'maroon'],
            'blue': ['blue', 'navy', 'royal blue', 'sky blue', 'teal', 'turquoise'],
            'green': ['green', 'emerald', 'forest green', 'lime', 'olive', 'mint'],
            'yellow': ['yellow', 'gold', 'lemon', 'mustard', 'amber'],
            'orange': ['orange', 'coral', 'peach', 'tangerine'],
            'purple': ['purple', 'violet', 'lavender', 'plum', 'magenta'],
            'pink': ['pink', 'rose', 'fuchsia', 'salmon'],
            'brown': ['brown', 'tan', 'beige', 'chocolate', 'coffee'],
            'black': ['black', 'charcoal', 'ebony'],
            'white': ['white', 'ivory', 'cream', 'off-white'],
            'gray': ['gray', 'grey', 'silver', 'slate']
        }
    
    def _load_style_keywords(self) -> Dict[str, List[str]]:
        """Load style and occasion keywords"""
        return {
            'casual': ['casual', 'everyday', 'relaxed', 'comfortable', 'laid-back'],
            'formal': ['formal', 'business', 'professional', 'office', 'work'],
            'party': ['party', 'night out', 'clubbing', 'evening', 'cocktail'],
            'sport': ['sport', 'athletic', 'workout', 'gym', 'running', 'fitness'],
            'vintage': ['vintage', 'retro', 'classic', 'old-school'],
            'trendy': ['trendy', 'fashionable', 'stylish', 'modern', 'contemporary']
        }
    
    async def enhance_voice_search(self, voice_query: str, confidence: float) -> Dict[str, Any]:
        """
        Enhance voice search using ML models
        
        Args:
            voice_query: The voice search query
            confidence: Voice recognition confidence
            
        Returns:
            Enhanced search parameters
        """
        try:
            # Extract fashion entities from voice query
            entities = self._extract_fashion_entities(voice_query)
            
            # Get semantic embeddings (mock implementation)
            embeddings = await self._get_query_embeddings(voice_query)
            
            # Generate search parameters
            search_params = self._generate_search_params(entities, embeddings)
            
            # Add ML-enhanced filters
            ml_filters = await self._generate_ml_filters(voice_query, entities)
            
            return {
                'original_query': voice_query,
                'confidence': confidence,
                'entities': entities,
                'search_params': search_params,
                'ml_filters': ml_filters,
                'enhanced_query': self._build_enhanced_query(entities),
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error enhancing voice search: {e}")
            return {
                'original_query': voice_query,
                'confidence': confidence,
                'error': str(e)
            }
    
    def _extract_fashion_entities(self, query: str) -> Dict[str, List[str]]:
        """Extract fashion-related entities from voice query"""
        query_lower = query.lower()
        entities = {
            'categories': [],
            'colors': [],
            'styles': [],
            'sizes': [],
            'brands': [],
            'materials': [],
            'occasions': []
        }
        
        # Extract categories
        for category, keywords in self.fashion_categories.items():
            for keyword in keywords:
                if keyword in query_lower:
                    entities['categories'].append(category)
        
        # Extract colors
        for color, variations in self.color_mappings.items():
            for variation in variations:
                if variation in query_lower:
                    entities['colors'].append(color)
        
        # Extract styles
        for style, keywords in self.style_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    entities['styles'].append(style)
        
        # Extract sizes (basic patterns)
        size_patterns = [
            r'\b(xs|extra small)\b',
            r'\b(s|small)\b',
            r'\b(m|medium)\b',
            r'\b(l|large)\b',
            r'\b(xl|extra large)\b',
            r'\b(xxl|2xl)\b',
            r'\bsize (\d+)\b'
        ]
        
        for pattern in size_patterns:
            matches = re.findall(pattern, query_lower)
            if matches:
                entities['sizes'].extend([match if isinstance(match, str) else match[0] for match in matches])
        
        # Extract price-related terms
        price_patterns = [
            r'\bunder (\d+)\b',
            r'\bless than (\d+)\b',
            r'\bcheap\b',
            r'\baffordable\b',
            r'\bexpensive\b',
            r'\bluxury\b'
        ]
        
        entities['price_hints'] = []
        for pattern in price_patterns:
            matches = re.findall(pattern, query_lower)
            if matches:
                entities['price_hints'].extend(matches)
        
        return entities
    
    async def _get_query_embeddings(self, query: str) -> Optional[np.ndarray]:
        """Get semantic embeddings for the query (mock implementation)"""
        try:
            # In a real implementation, this would call your ML service
            # For now, return a mock embedding
            return np.random.rand(128)  # Mock 128-dimensional embedding
        
        except Exception as e:
            logger.error(f"Error getting query embeddings: {e}")
            return None
    
    def _generate_search_params(self, entities: Dict[str, List[str]], embeddings: Optional[np.ndarray]) -> Dict[str, Any]:
        """Generate enhanced search parameters"""
        params = {
            'categories': list(set(entities['categories'])),
            'colors': list(set(entities['colors'])),
            'styles': list(set(entities['styles'])),
            'sizes': list(set(entities['sizes']))
        }
        
        # Add semantic similarity if embeddings are available
        if embeddings is not None:
            params['use_semantic_search'] = True
            params['embedding_vector'] = embeddings.tolist()
        
        return params
    
    async def _generate_ml_filters(self, query: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Generate ML-enhanced filters"""
        filters = {}
        
        # Style-based filters
        if entities['styles']:
            filters['style_confidence'] = await self._calculate_style_confidence(entities['styles'])
        
        # Color harmony suggestions
        if entities['colors']:
            filters['color_harmony'] = await self._suggest_color_harmony(entities['colors'])
        
        # Size recommendations
        if entities['sizes']:
            filters['size_recommendations'] = await self._get_size_recommendations(entities['sizes'])
        
        # Occasion-based filtering
        occasion_hints = self._extract_occasion_hints(query)
        if occasion_hints:
            filters['occasion_filters'] = occasion_hints
        
        return filters
    
    async def _calculate_style_confidence(self, styles: List[str]) -> Dict[str, float]:
        """Calculate confidence scores for detected styles"""
        # Mock implementation
        return {style: 0.8 + (len(style) * 0.02) for style in styles}
    
    async def _suggest_color_harmony(self, colors: List[str]) -> Dict[str, List[str]]:
        """Suggest complementary colors based on color theory"""
        color_harmony = {
            'red': ['white', 'black', 'gray', 'blue'],
            'blue': ['white', 'gray', 'yellow', 'orange'],
            'green': ['brown', 'beige', 'white', 'black'],
            'yellow': ['blue', 'purple', 'gray', 'black'],
            'orange': ['blue', 'brown', 'white'],
            'purple': ['yellow', 'white', 'gray'],
            'pink': ['gray', 'white', 'black', 'green'],
            'brown': ['cream', 'white', 'orange'],
            'black': ['white', 'red', 'yellow'],
            'white': ['black', 'blue', 'red'],
            'gray': ['yellow', 'pink', 'blue']
        }
        
        suggestions = {}
        for color in colors:
            if color in color_harmony:
                suggestions[color] = color_harmony[color]
        
        return suggestions
    
    async def _get_size_recommendations(self, sizes: List[str]) -> Dict[str, Any]:
        """Get size recommendations and size chart info"""
        # Mock implementation
        return {
            'recommended_sizes': sizes,
            'size_chart_available': True,
            'fit_guide': 'Check our size guide for accurate measurements'
        }
    
    def _extract_occasion_hints(self, query: str) -> List[str]:
        """Extract occasion hints from the query"""
        occasions = {
            'work': ['work', 'office', 'business', 'professional', 'meeting'],
            'casual': ['casual', 'everyday', 'weekend', 'relaxed'],
            'party': ['party', 'night out', 'clubbing', 'celebration'],
            'wedding': ['wedding', 'formal event', 'ceremony'],
            'vacation': ['vacation', 'holiday', 'beach', 'travel'],
            'sport': ['sport', 'gym', 'workout', 'running', 'fitness']
        }
        
        detected_occasions = []
        query_lower = query.lower()
        
        for occasion, keywords in occasions.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_occasions.append(occasion)
        
        return detected_occasions
    
    def _build_enhanced_query(self, entities: Dict[str, List[str]]) -> str:
        """Build an enhanced search query from extracted entities"""
        query_parts = []
        
        if entities['categories']:
            query_parts.extend(entities['categories'])
        
        if entities['colors']:
            query_parts.extend(entities['colors'])
        
        if entities['styles']:
            query_parts.extend(entities['styles'])
        
        return ' '.join(query_parts)
    
    async def get_voice_recommendations(self, user_id: str, voice_history: List[str]) -> Dict[str, Any]:
        """Get personalized recommendations based on voice command history"""
        try:
            # Analyze voice command patterns
            patterns = self._analyze_voice_patterns(voice_history)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(user_id, patterns)
            
            return {
                'user_id': user_id,
                'patterns': patterns,
                'recommendations': recommendations,
                'generated_at': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error generating voice recommendations: {e}")
            return {'error': str(e)}
    
    def _analyze_voice_patterns(self, voice_history: List[str]) -> Dict[str, Any]:
        """Analyze patterns in voice command history"""
        patterns = {
            'frequent_categories': [],
            'preferred_colors': [],
            'search_times': [],
            'query_complexity': 0
        }
        
        all_entities = []
        for query in voice_history:
            entities = self._extract_fashion_entities(query)
            all_entities.append(entities)
        
        # Find most frequent categories
        category_counts = {}
        for entities in all_entities:
            for category in entities['categories']:
                category_counts[category] = category_counts.get(category, 0) + 1
        
        patterns['frequent_categories'] = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Find preferred colors
        color_counts = {}
        for entities in all_entities:
            for color in entities['colors']:
                color_counts[color] = color_counts.get(color, 0) + 1
        
        patterns['preferred_colors'] = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Calculate average query complexity
        if voice_history:
            total_words = sum(len(query.split()) for query in voice_history)
            patterns['query_complexity'] = total_words / len(voice_history)
        
        return patterns
    
    async def _generate_recommendations(self, user_id: str, patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Recommend based on frequent categories
        for category, count in patterns['frequent_categories'][:3]:
            recommendations.append({
                'type': 'category_based',
                'category': category,
                'reason': f'You frequently search for {category} items',
                'confidence': min(0.9, 0.5 + (count * 0.1))
            })
        
        # Recommend complementary colors
        for color, count in patterns['preferred_colors'][:2]:
            harmony = await self._suggest_color_harmony([color])
            if color in harmony:
                for complement in harmony[color][:2]:
                    recommendations.append({
                        'type': 'color_harmony',
                        'base_color': color,
                        'recommended_color': complement,
                        'reason': f'{complement} complements your preferred {color} items',
                        'confidence': 0.7
                    })
        
        return recommendations
    
    def update_user_preferences(self, user_id: str, voice_command: str, action_taken: bool):
        """Update user preferences based on voice command success"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                'successful_commands': [],
                'failed_commands': [],
                'preferences_updated': datetime.now()
            }
        
        if action_taken:
            self.user_preferences[user_id]['successful_commands'].append({
                'command': voice_command,
                'timestamp': datetime.now().isoformat()
            })
        else:
            self.user_preferences[user_id]['failed_commands'].append({
                'command': voice_command,
                'timestamp': datetime.now().isoformat()
            })
        
        # Keep only recent history (last 100 commands)
        for key in ['successful_commands', 'failed_commands']:
            if len(self.user_preferences[user_id][key]) > 100:
                self.user_preferences[user_id][key] = self.user_preferences[user_id][key][-100:]
    
    def get_voice_analytics(self) -> Dict[str, Any]:
        """Get analytics about voice command usage"""
        total_users = len(self.user_preferences)
        total_commands = 0
        successful_commands = 0
        
        category_usage = {}
        color_usage = {}
        
        for user_data in self.user_preferences.values():
            user_successful = len(user_data['successful_commands'])
            user_failed = len(user_data['failed_commands'])
            
            total_commands += user_successful + user_failed
            successful_commands += user_successful
            
            # Analyze command content
            all_user_commands = [cmd['command'] for cmd in user_data['successful_commands']] + \
                              [cmd['command'] for cmd in user_data['failed_commands']]
            
            for command in all_user_commands:
                entities = self._extract_fashion_entities(command)
                
                for category in entities['categories']:
                    category_usage[category] = category_usage.get(category, 0) + 1
                
                for color in entities['colors']:
                    color_usage[color] = color_usage.get(color, 0) + 1
        
        success_rate = successful_commands / total_commands if total_commands > 0 else 0
        
        return {
            'total_users': total_users,
            'total_commands': total_commands,
            'success_rate': success_rate,
            'popular_categories': sorted(category_usage.items(), key=lambda x: x[1], reverse=True)[:10],
            'popular_colors': sorted(color_usage.items(), key=lambda x: x[1], reverse=True)[:10],
            'analytics_generated': datetime.now().isoformat()
        }
