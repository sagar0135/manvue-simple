"""
Text-to-Speech Module for ManVue Application

This module provides text-to-speech functionality for voice feedback and accessibility.
"""

import pyttsx3
import logging
import threading
import queue
import time
from typing import Optional, Dict, Any, List
from ..config.voice_config import config

logger = logging.getLogger(__name__)

class TextToSpeech:
    """Text-to-speech engine for providing audio feedback"""
    
    def __init__(self):
        """Initialize the text-to-speech engine"""
        self.engine = None
        self.is_initialized = False
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.speech_thread = None
        self.enabled = True
        
        self._initialize_engine()
        self._start_speech_worker()
        
        logger.info("Text-to-speech engine initialized")
    
    def _initialize_engine(self):
        """Initialize the TTS engine with configuration"""
        try:
            self.engine = pyttsx3.init()
            
            # Configure voice properties
            self.engine.setProperty('rate', config.TTS_RATE)
            self.engine.setProperty('volume', config.TTS_VOLUME)
            
            # Try to set a pleasant voice
            voices = self.engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.engine.setProperty('voice', voices[0].id)
            
            self.is_initialized = True
            logger.info("TTS engine configured successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.is_initialized = False
    
    def _start_speech_worker(self):
        """Start the background thread for speech processing"""
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
    
    def _speech_worker(self):
        """Background worker to process speech queue"""
        while True:
            try:
                speech_data = self.speech_queue.get(timeout=1)
                if speech_data is None:  # Shutdown signal
                    break
                
                self._speak_text(speech_data)
                self.speech_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in speech worker: {e}")
    
    def speak(self, text: str, priority: int = 0, interrupt: bool = False):
        """
        Queue text for speech synthesis
        
        Args:
            text: Text to speak
            priority: Priority level (higher = more urgent)
            interrupt: Whether to interrupt current speech
        """
        if not self.enabled or not self.is_initialized or not text.strip():
            return
        
        if interrupt:
            self.stop_speaking()
        
        speech_data = {
            'text': text.strip(),
            'priority': priority,
            'timestamp': time.time()
        }
        
        self.speech_queue.put(speech_data)
        logger.debug(f"Queued for speech: '{text[:50]}...'")
    
    def _speak_text(self, speech_data: Dict[str, Any]):
        """Actually speak the text using the TTS engine"""
        try:
            text = speech_data['text']
            self.is_speaking = True
            
            logger.debug(f"Speaking: '{text[:50]}...'")
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            logger.error(f"Error speaking text: {e}")
        finally:
            self.is_speaking = False
    
    def stop_speaking(self):
        """Stop current speech and clear queue"""
        if self.is_initialized and self.engine:
            try:
                self.engine.stop()
            except:
                pass
        
        # Clear the queue
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
                self.speech_queue.task_done()
            except queue.Empty:
                break
        
        self.is_speaking = False
        logger.debug("Speech stopped and queue cleared")
    
    def set_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        if self.is_initialized and self.engine:
            try:
                self.engine.setProperty('rate', rate)
                logger.debug(f"Speech rate set to {rate} WPM")
            except Exception as e:
                logger.error(f"Error setting speech rate: {e}")
    
    def set_volume(self, volume: float):
        """Set speech volume (0.0 to 1.0)"""
        if self.is_initialized and self.engine:
            try:
                volume = max(0.0, min(1.0, volume))  # Clamp to valid range
                self.engine.setProperty('volume', volume)
                logger.debug(f"Speech volume set to {volume}")
            except Exception as e:
                logger.error(f"Error setting speech volume: {e}")
    
    def set_voice(self, voice_id: str):
        """Set voice by ID"""
        if self.is_initialized and self.engine:
            try:
                self.engine.setProperty('voice', voice_id)
                logger.debug(f"Voice set to {voice_id}")
            except Exception as e:
                logger.error(f"Error setting voice: {e}")
    
    def get_voices(self) -> List[Dict[str, str]]:
        """Get list of available voices"""
        if not self.is_initialized or not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [
                {
                    'id': voice.id,
                    'name': voice.name,
                    'gender': getattr(voice, 'gender', 'unknown'),
                    'age': getattr(voice, 'age', 'unknown')
                }
                for voice in voices
            ] if voices else []
        except Exception as e:
            logger.error(f"Error getting voices: {e}")
            return []
    
    def enable(self):
        """Enable text-to-speech"""
        self.enabled = True
        logger.info("Text-to-speech enabled")
    
    def disable(self):
        """Disable text-to-speech"""
        self.enabled = False
        self.stop_speaking()
        logger.info("Text-to-speech disabled")
    
    def is_enabled(self) -> bool:
        """Check if TTS is enabled"""
        return self.enabled and self.is_initialized
    
    def get_status(self) -> Dict[str, Any]:
        """Get current TTS status"""
        return {
            'enabled': self.enabled,
            'initialized': self.is_initialized,
            'speaking': self.is_speaking,
            'queue_size': self.speech_queue.qsize(),
            'available_voices': len(self.get_voices())
        }
    
    def speak_command_feedback(self, action: str, success: bool = True, details: str = ""):
        """Provide audio feedback for voice commands"""
        if not self.enabled:
            return
        
        feedback_messages = {
            'navigate_to_page': "Navigating to page",
            'search_products': "Searching for products",
            'add_to_cart': "Added to cart" if success else "Could not add to cart",
            'open_cart': "Opening shopping cart",
            'show_product_details': "Showing product details",
            'filter_by_category': "Filtering by category",
            'filter_by_color': "Filtering by color",
            'filter_by_price': "Filtering by price",
            'read_page_content': "Reading page content",
            'describe_image': "Describing image",
            'show_voice_help': "Here are the available voice commands"
        }
        
        message = feedback_messages.get(action, f"Executing {action}")
        if details:
            message += f": {details}"
        
        self.speak(message, priority=1)
    
    def speak_error(self, error_message: str):
        """Speak error messages with appropriate tone"""
        self.speak(f"Sorry, {error_message}", priority=2, interrupt=True)
    
    def speak_welcome(self):
        """Speak welcome message"""
        message = "Welcome to ManVue. Voice commands are now active. Say 'help' to hear available commands."
        self.speak(message, priority=3)
    
    def speak_help(self):
        """Speak help information"""
        help_text = """
        You can use the following voice commands:
        Say 'go home' to return to the main page.
        Say 'search for' followed by a product name to search.
        Say 'show products' to view the catalog.
        Say 'open cart' to view your shopping cart.
        Say 'add to cart' when viewing a product.
        Say 'help' to repeat this message.
        """
        self.speak(help_text, priority=3)
    
    def shutdown(self):
        """Shutdown the TTS engine"""
        self.enabled = False
        self.stop_speaking()
        
        # Signal speech worker to stop
        self.speech_queue.put(None)
        
        if self.speech_thread and self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2)
        
        if self.engine:
            try:
                del self.engine
            except:
                pass
        
        logger.info("Text-to-speech engine shutdown")
