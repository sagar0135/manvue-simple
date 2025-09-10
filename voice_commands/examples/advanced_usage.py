#!/usr/bin/env python3
"""
Advanced Voice Commands Usage Example for ManVue Application

This example demonstrates advanced usage of the voice commands system including:
- Custom command registration
- Voice analytics
- ML integration
- WebSocket communication
- Custom action handlers

Run this script to see advanced voice command functionality in action.
"""

import asyncio
import logging
import json
import time
from typing import Dict, Any, List
import websockets
import threading

# Import voice command modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.voice_recognizer import VoiceRecognizer
from core.command_processor import CommandProcessor
from core.text_to_speech import TextToSpeech
from integration.ml_voice_integration import VoiceMLIntegration
from config.voice_config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AdvancedVoiceExample:
    """Advanced example demonstrating voice command capabilities"""
    
    def __init__(self):
        self.voice_recognizer = None
        self.command_processor = None
        self.tts_engine = None
        self.ml_integration = None
        self.is_running = False
        self.command_history = []
        self.user_id = "demo_user"
        
    async def initialize(self):
        """Initialize all voice components"""
        try:
            logger.info("Initializing advanced voice example...")
            
            # Initialize core components
            self.command_processor = CommandProcessor()
            self.tts_engine = TextToSpeech()
            self.ml_integration = VoiceMLIntegration()
            
            # Register custom action handlers
            self.register_custom_handlers()
            
            # Add custom commands
            self.add_custom_commands()
            
            logger.info("Advanced voice example initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize voice example: {e}")
            return False
    
    def register_custom_handlers(self):
        """Register custom action handlers for demonstration"""
        
        def handle_product_search(action_data):
            """Enhanced product search with ML integration"""
            query = action_data['parameters'].get('query', '')
            logger.info(f"🔍 Searching for products: {query}")
            
            # Simulate ML-enhanced search
            enhanced_results = {
                'query': query,
                'results_found': 25,
                'ml_suggestions': ['red dress', 'blue dress', 'evening dress'],
                'categories': ['dresses', 'formal wear'],
                'price_range': '$25 - $150'
            }
            
            # Provide TTS feedback
            if self.tts_engine:
                feedback = f"Found {enhanced_results['results_found']} products for {query}"
                self.tts_engine.speak(feedback)
            
            return enhanced_results
        
        def handle_smart_recommendation(action_data):
            """Handle smart product recommendations"""
            style = action_data['parameters'].get('style', 'casual')
            logger.info(f"🎯 Getting recommendations for {style} style")
            
            recommendations = {
                'style': style,
                'recommended_items': [
                    {'name': 'Blue Cotton Shirt', 'price': '$45', 'match_score': 0.92},
                    {'name': 'Dark Jeans', 'price': '$65', 'match_score': 0.88},
                    {'name': 'White Sneakers', 'price': '$85', 'match_score': 0.85}
                ]
            }
            
            # Provide detailed TTS feedback
            if self.tts_engine:
                feedback = f"Here are my top recommendations for {style} style: "
                for item in recommendations['recommended_items'][:2]:
                    feedback += f"{item['name']} for {item['price']}, "
                self.tts_engine.speak(feedback)
            
            return recommendations
        
        def handle_voice_analytics(action_data):
            """Show voice usage analytics"""
            logger.info("📊 Generating voice analytics")
            
            analytics = {
                'total_commands': len(self.command_history),
                'most_used_commands': self.get_popular_commands(),
                'success_rate': 0.85,
                'favorite_categories': ['dresses', 'shoes', 'accessories']
            }
            
            if self.tts_engine:
                feedback = f"You've used {analytics['total_commands']} voice commands with an {analytics['success_rate']*100}% success rate"
                self.tts_engine.speak(feedback)
            
            return analytics
        
        def handle_style_advice(action_data):
            """Provide style advice based on ML analysis"""
            occasion = action_data['parameters'].get('occasion', 'casual')
            logger.info(f"👗 Providing style advice for {occasion} occasion")
            
            advice = {
                'occasion': occasion,
                'color_palette': ['navy blue', 'white', 'beige'],
                'style_tips': [
                    'Layer with a light cardigan',
                    'Accessorize with simple jewelry',
                    'Choose comfortable but stylish shoes'
                ],
                'must_have_items': ['white button-down shirt', 'dark jeans', 'black blazer']
            }
            
            if self.tts_engine:
                feedback = f"For {occasion} occasions, I recommend focusing on {', '.join(advice['color_palette'][:2])} colors"
                self.tts_engine.speak(feedback)
            
            return advice
        
        # Register handlers
        handlers = {
            'search_products': handle_product_search,
            'smart_recommendation': handle_smart_recommendation,
            'voice_analytics': handle_voice_analytics,
            'style_advice': handle_style_advice
        }
        
        for action, handler in handlers.items():
            self.command_processor.register_action_handler(action, handler)
            logger.info(f"Registered handler for: {action}")
    
    def add_custom_commands(self):
        """Add custom commands to the processor"""
        custom_commands = [
            {
                'pattern': 'recommend * style',
                'action': 'smart_recommendation',
                'parameters': {'type': 'style_based'}
            },
            {
                'pattern': 'show my stats',
                'action': 'voice_analytics',
                'parameters': {}
            },
            {
                'pattern': 'style advice for *',
                'action': 'style_advice',
                'parameters': {}
            },
            {
                'pattern': 'what should I wear for *',
                'action': 'style_advice',
                'parameters': {}
            }
        ]
        
        for cmd in custom_commands:
            # Add to processor's custom commands
            if not hasattr(self.command_processor, 'custom_commands'):
                self.command_processor.custom_commands = []
            
            self.command_processor.custom_commands.append(cmd)
            logger.info(f"Added custom command: {cmd['pattern']}")
    
    async def run_voice_recognition_demo(self):
        """Run voice recognition demonstration"""
        logger.info("🎤 Starting voice recognition demo...")
        
        if self.tts_engine:
            self.tts_engine.speak("Voice recognition demo started. Try saying a command.")
        
        # Simulate voice commands for demo
        demo_commands = [
            "search for red dress",
            "recommend casual style",
            "show my stats",
            "what should I wear for work",
            "style advice for party",
            "find blue jeans",
            "show me sneakers"
        ]
        
        for i, command in enumerate(demo_commands):
            logger.info(f"\n--- Demo Command {i+1}: '{command}' ---")
            
            # Process command
            result = self.command_processor.process_command(command, 0.9)
            
            if result:
                logger.info(f"✅ Command processed successfully")
                logger.info(f"Action: {result['action']}")
                logger.info(f"Parameters: {result['parameters']}")
                
                # Add to history
                self.command_history.append({
                    'command': command,
                    'result': result,
                    'timestamp': time.time(),
                    'success': True
                })
                
                # Update ML preferences
                if self.ml_integration:
                    self.ml_integration.update_user_preferences(self.user_id, command, True)
            
            else:
                logger.info(f"❌ Command not recognized: {command}")
                self.command_history.append({
                    'command': command,
                    'result': None,
                    'timestamp': time.time(),
                    'success': False
                })
            
            # Wait between commands
            await asyncio.sleep(2)
    
    async def run_ml_integration_demo(self):
        """Demonstrate ML integration features"""
        logger.info("🤖 Starting ML integration demo...")
        
        if self.tts_engine:
            self.tts_engine.speak("Starting machine learning integration demo")
        
        # Test voice search enhancement
        test_queries = [
            "red summer dress for beach vacation",
            "professional outfit for business meeting",
            "casual weekend clothes"
        ]
        
        for query in test_queries:
            logger.info(f"\n--- ML Enhancement for: '{query}' ---")
            
            enhanced_result = await self.ml_integration.enhance_voice_search(query, 0.85)
            
            logger.info(f"Enhanced search result:")
            logger.info(f"  Entities: {enhanced_result.get('entities', {})}")
            logger.info(f"  Search params: {enhanced_result.get('search_params', {})}")
            logger.info(f"  ML filters: {enhanced_result.get('ml_filters', {})}")
            
            await asyncio.sleep(1)
        
        # Generate recommendations
        logger.info("\n--- Generating Personalized Recommendations ---")
        voice_history = [cmd['command'] for cmd in self.command_history if cmd['success']]
        
        recommendations = await self.ml_integration.get_voice_recommendations(
            self.user_id, voice_history
        )
        
        logger.info(f"Recommendations based on voice history:")
        for rec in recommendations.get('recommendations', [])[:3]:
            logger.info(f"  - {rec.get('reason', 'No reason')}")
    
    def get_popular_commands(self) -> List[Dict[str, Any]]:
        """Get most popular commands from history"""
        command_counts = {}
        
        for entry in self.command_history:
            if entry['success']:
                cmd = entry['command']
                command_counts[cmd] = command_counts.get(cmd, 0) + 1
        
        return sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    async def websocket_demo(self):
        """Demonstrate WebSocket communication (mock)"""
        logger.info("🌐 WebSocket communication demo...")
        
        # Mock WebSocket messages
        mock_messages = [
            {'type': 'voice_command', 'text': 'search for shoes', 'confidence': 0.9},
            {'type': 'get_commands'},
            {'type': 'start_listening'},
            {'type': 'stop_listening'}
        ]
        
        for message in mock_messages:
            logger.info(f"Mock WebSocket message: {message}")
            
            # Simulate message processing
            if message['type'] == 'voice_command':
                result = self.command_processor.process_command(
                    message['text'], message['confidence']
                )
                logger.info(f"WebSocket response: {result}")
            
            elif message['type'] == 'get_commands':
                commands = self.command_processor.get_available_commands()
                logger.info(f"Available commands: {len(commands)} commands")
            
            await asyncio.sleep(1)
    
    def display_analytics(self):
        """Display comprehensive analytics"""
        logger.info("\n📊 === VOICE ANALYTICS SUMMARY ===")
        logger.info(f"Total commands processed: {len(self.command_history)}")
        
        successful_commands = [cmd for cmd in self.command_history if cmd['success']]
        success_rate = len(successful_commands) / len(self.command_history) if self.command_history else 0
        logger.info(f"Success rate: {success_rate:.2%}")
        
        popular_commands = self.get_popular_commands()
        logger.info(f"Most popular commands:")
        for cmd, count in popular_commands:
            logger.info(f"  - '{cmd}': {count} times")
        
        # ML analytics
        if self.ml_integration:
            ml_analytics = self.ml_integration.get_voice_analytics()
            logger.info(f"ML Analytics:")
            logger.info(f"  - Total users: {ml_analytics.get('total_users', 0)}")
            logger.info(f"  - Popular categories: {ml_analytics.get('popular_categories', [])[:3]}")
    
    async def run_complete_demo(self):
        """Run the complete demonstration"""
        if not await self.initialize():
            logger.error("Failed to initialize. Exiting.")
            return
        
        logger.info("🚀 Starting Advanced Voice Commands Demo")
        logger.info("=" * 50)
        
        try:
            # Run different demo sections
            await self.run_voice_recognition_demo()
            await asyncio.sleep(2)
            
            await self.run_ml_integration_demo()
            await asyncio.sleep(2)
            
            await self.websocket_demo()
            await asyncio.sleep(1)
            
            # Display final analytics
            self.display_analytics()
            
            logger.info("\n✅ Demo completed successfully!")
            
            if self.tts_engine:
                self.tts_engine.speak("Demo completed successfully!")
        
        except Exception as e:
            logger.error(f"Demo error: {e}")
        
        finally:
            # Cleanup
            if self.tts_engine:
                self.tts_engine.shutdown()

async def main():
    """Main function to run the advanced example"""
    demo = AdvancedVoiceExample()
    await demo.run_complete_demo()

if __name__ == "__main__":
    print("🎤 ManVue Advanced Voice Commands Demo")
    print("=" * 40)
    print("This demo shows advanced voice command features including:")
    print("- Custom command handlers")
    print("- ML-enhanced search")
    print("- Voice analytics")
    print("- WebSocket communication")
    print("- Text-to-speech feedback")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        logger.exception("Demo exception:")
    
    print("\n🏁 Demo finished")
