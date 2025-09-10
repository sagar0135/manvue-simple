"""
Voice Command Processor for ManVue Application

This module processes natural language voice commands and executes corresponding actions.
"""

import json
import re
import logging
from typing import Dict, List, Optional, Any, Callable
from difflib import SequenceMatcher
import os
from ..config.voice_config import config

logger = logging.getLogger(__name__)

class CommandProcessor:
    """Processes voice commands and executes corresponding actions"""
    
    def __init__(self, commands_config_path: Optional[str] = None):
        """
        Initialize the command processor
        
        Args:
            commands_config_path: Path to commands configuration file
        """
        self.commands_config = {}
        self.action_handlers = {}
        self.context = {}
        self.last_command = None
        
        # Load commands configuration
        if commands_config_path is None:
            commands_config_path = os.path.join(
                os.path.dirname(__file__), 
                "..", "config", "commands_config.json"
            )
        
        self.load_commands_config(commands_config_path)
        self._register_default_handlers()
        
        logger.info("Command processor initialized")
    
    def load_commands_config(self, config_path: str):
        """Load voice commands configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.commands_config = json.load(f)
            logger.info(f"Loaded commands configuration from {config_path}")
        except FileNotFoundError:
            logger.error(f"Commands configuration file not found: {config_path}")
            self.commands_config = {"voice_commands": {}}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in commands configuration: {e}")
            self.commands_config = {"voice_commands": {}}
    
    def register_action_handler(self, action: str, handler: Callable):
        """
        Register a handler function for a specific action
        
        Args:
            action: The action name (e.g., 'navigate_to_page')
            handler: Function to call when action is triggered
        """
        self.action_handlers[action] = handler
        logger.debug(f"Registered handler for action: {action}")
    
    def process_command(self, text: str, confidence: float) -> Optional[Dict[str, Any]]:
        """
        Process a voice command and return the action to execute
        
        Args:
            text: The recognized text
            confidence: Recognition confidence score
            
        Returns:
            Dict containing action and parameters, or None if no match
        """
        text = text.strip().lower()
        
        if not text:
            return None
        
        logger.info(f"Processing command: '{text}' (confidence: {confidence})")
        
        # Find best matching command
        best_match = self._find_best_command_match(text)
        
        if best_match:
            command_info = best_match['command_info']
            match_confidence = best_match['confidence']
            extracted_params = best_match.get('parameters', {})
            
            # Check if confidence meets threshold for this command category
            category = best_match['category']
            threshold = self.commands_config.get('confidence_thresholds', {}).get(category, 0.7)
            
            if match_confidence >= threshold and confidence >= config.CONFIDENCE_THRESHOLD:
                # Prepare action data
                action_data = {
                    'action': command_info['action'],
                    'parameters': {**command_info.get('parameters', {}), **extracted_params},
                    'original_text': text,
                    'confidence': confidence,
                    'match_confidence': match_confidence,
                    'category': category
                }
                
                # Store for context
                self.last_command = action_data
                
                # Execute action if handler is registered
                if command_info['action'] in self.action_handlers:
                    try:
                        result = self.action_handlers[command_info['action']](action_data)
                        action_data['result'] = result
                    except Exception as e:
                        logger.error(f"Error executing action {command_info['action']}: {e}")
                        action_data['error'] = str(e)
                
                return action_data
            else:
                logger.debug(f"Command confidence too low: {match_confidence} < {threshold}")
        
        # Try to handle as a general search if no specific command matched
        if self._looks_like_search(text):
            return self._handle_general_search(text, confidence)
        
        logger.debug(f"No matching command found for: '{text}'")
        return None
    
    def _find_best_command_match(self, text: str) -> Optional[Dict[str, Any]]:
        """Find the best matching command for the given text"""
        best_match = None
        best_score = 0
        
        voice_commands = self.commands_config.get('voice_commands', {})
        
        for category, commands in voice_commands.items():
            for command_name, command_info in commands.items():
                patterns = command_info.get('patterns', [])
                
                for pattern in patterns:
                    match_result = self._match_pattern(text, pattern)
                    
                    if match_result['score'] > best_score:
                        best_score = match_result['score']
                        best_match = {
                            'category': category,
                            'command_name': command_name,
                            'command_info': command_info,
                            'confidence': match_result['score'],
                            'parameters': match_result.get('parameters', {})
                        }
        
        return best_match if best_score > 0.6 else None
    
    def _match_pattern(self, text: str, pattern: str) -> Dict[str, Any]:
        """Match text against a command pattern and extract parameters"""
        # Convert pattern to regex for parameter extraction
        regex_pattern = pattern
        parameters = {}
        
        # Find parameters in curly braces
        param_matches = re.findall(r'\{(\w+)\}', pattern)
        
        # Replace parameters with capture groups
        for param in param_matches:
            if param in ['product', 'item']:
                # Match product names (allowing multiple words)
                regex_pattern = regex_pattern.replace(f'{{{param}}}', r'(.+?)')
            elif param in ['category']:
                # Match categories
                categories = '|'.join(self.commands_config.get('categories', ['.*']))
                regex_pattern = regex_pattern.replace(f'{{{param}}}', f'({categories})')
            elif param in ['color']:
                # Match colors
                colors = '|'.join(self.commands_config.get('colors', ['.*']))
                regex_pattern = regex_pattern.replace(f'{{{param}}}', f'({colors})')
            elif param in ['size']:
                # Match sizes
                sizes = '|'.join(self.commands_config.get('sizes', ['.*']))
                regex_pattern = regex_pattern.replace(f'{{{param}}}', f'({sizes})')
            elif param in ['price', 'amount']:
                # Match prices/amounts
                regex_pattern = regex_pattern.replace(f'{{{param}}}', r'(\\d+(?:\\.\\d{2})?|cheap|affordable|expensive)')
            else:
                # Generic parameter matching
                regex_pattern = regex_pattern.replace(f'{{{param}}}', r'(.+?)')
        
        # Try exact regex match first
        regex_match = re.search(f'^{regex_pattern}$', text, re.IGNORECASE)
        if regex_match:
            # Extract parameters
            for i, param in enumerate(param_matches):
                if i < len(regex_match.groups()):
                    parameters[param] = regex_match.group(i + 1).strip()
            
            return {
                'score': 1.0,
                'parameters': parameters
            }
        
        # Fallback to similarity matching
        similarity = SequenceMatcher(None, text, pattern.lower()).ratio()
        
        # Boost score if key words match
        pattern_words = set(re.sub(r'\{.*?\}', '', pattern).split())
        text_words = set(text.split())
        word_overlap = len(pattern_words.intersection(text_words)) / max(len(pattern_words), 1)
        
        final_score = (similarity * 0.7) + (word_overlap * 0.3)
        
        return {
            'score': final_score,
            'parameters': parameters
        }
    
    def _looks_like_search(self, text: str) -> bool:
        """Check if text looks like a search query"""
        search_indicators = [
            'search', 'find', 'look for', 'show me', 'where is',
            'display', 'get', 'bring up'
        ]
        return any(indicator in text for indicator in search_indicators)
    
    def _handle_general_search(self, text: str, confidence: float) -> Dict[str, Any]:
        """Handle general search queries"""
        # Extract search terms (remove common command words)
        search_words = ['search', 'for', 'find', 'look', 'show', 'me', 'where', 'is', 'the']
        search_terms = ' '.join([word for word in text.split() if word not in search_words])
        
        return {
            'action': 'search_products',
            'parameters': {
                'query': search_terms,
                'type': 'general_search'
            },
            'original_text': text,
            'confidence': confidence,
            'match_confidence': 0.8,
            'category': 'search'
        }
    
    def _register_default_handlers(self):
        """Register default action handlers"""
        
        def log_action(action_data):
            logger.info(f"Executing action: {action_data['action']} with parameters: {action_data['parameters']}")
            return {"status": "logged"}
        
        # Register a default logger for all actions
        default_actions = [
            'navigate_to_page', 'search_products', 'add_to_cart', 'open_cart',
            'show_product_details', 'filter_by_category', 'filter_by_color',
            'filter_by_price', 'filter_by_size', 'filter_by_brand',
            'read_page_content', 'describe_image', 'navigate_next_item',
            'navigate_previous_item', 'show_voice_help', 'start_voice_recognition',
            'stop_voice_recognition', 'add_to_comparison'
        ]
        
        for action in default_actions:
            if action not in self.action_handlers:
                self.action_handlers[action] = log_action
    
    def get_context(self) -> Dict[str, Any]:
        """Get current command processing context"""
        return {
            'last_command': self.last_command,
            'context': self.context
        }
    
    def set_context(self, key: str, value: Any):
        """Set context value for command processing"""
        self.context[key] = value
    
    def get_available_commands(self) -> List[str]:
        """Get list of all available voice commands"""
        commands = []
        voice_commands = self.commands_config.get('voice_commands', {})
        
        for category, command_dict in voice_commands.items():
            for command_name, command_info in command_dict.items():
                patterns = command_info.get('patterns', [])
                commands.extend(patterns)
        
        return sorted(commands)
    
    def clear_context(self):
        """Clear command processing context"""
        self.context.clear()
        self.last_command = None
