"""
Voice Recognition Module for ManVue Application

This module handles speech-to-text conversion using various speech recognition engines.
"""

import speech_recognition as sr
import logging
import threading
import time
from typing import Optional, Callable, Dict, Any
import queue
import json
import os
from ..config.voice_config import config

logger = logging.getLogger(__name__)

class VoiceRecognizer:
    """Main voice recognition class that handles speech-to-text conversion"""
    
    def __init__(self, 
                 microphone_index: Optional[int] = None,
                 callback: Optional[Callable[[str, float], None]] = None):
        """
        Initialize the voice recognizer
        
        Args:
            microphone_index: Index of microphone to use (None for default)
            callback: Function to call when speech is recognized
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=microphone_index)
        self.callback = callback
        self.is_listening = False
        self.listen_thread = None
        self.command_queue = queue.Queue()
        
        # Configure recognizer settings
        self.recognizer.energy_threshold = config.ENERGY_THRESHOLD
        self.recognizer.phrase_threshold = config.PHRASE_TIMEOUT
        self.recognizer.timeout = config.RECOGNITION_TIMEOUT
        
        # Calibrate microphone for ambient noise
        self._calibrate_microphone()
        
        logger.info("Voice recognizer initialized")
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise levels"""
        try:
            with self.microphone as source:
                logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info(f"Microphone calibrated. Energy threshold: {self.recognizer.energy_threshold}")
        except Exception as e:
            logger.error(f"Failed to calibrate microphone: {e}")
    
    def start_listening(self) -> bool:
        """
        Start continuous listening for voice commands
        
        Returns:
            bool: True if listening started successfully, False otherwise
        """
        if self.is_listening:
            logger.warning("Already listening for voice commands")
            return True
        
        try:
            self.is_listening = True
            self.listen_thread = threading.Thread(target=self._listen_continuously)
            self.listen_thread.daemon = True
            self.listen_thread.start()
            logger.info("Started listening for voice commands")
            return True
        except Exception as e:
            logger.error(f"Failed to start listening: {e}")
            self.is_listening = False
            return False
    
    def stop_listening(self):
        """Stop listening for voice commands"""
        if not self.is_listening:
            return
        
        self.is_listening = False
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2)
        logger.info("Stopped listening for voice commands")
    
    def _listen_continuously(self):
        """Continuously listen for voice commands in a separate thread"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                if not self.is_listening:
                    break
                
                # Process audio in background thread
                threading.Thread(
                    target=self._process_audio,
                    args=(audio,),
                    daemon=True
                ).start()
                
            except sr.WaitTimeoutError:
                # Timeout is normal during continuous listening
                continue
            except Exception as e:
                logger.error(f"Error during continuous listening: {e}")
                time.sleep(0.1)
    
    def _process_audio(self, audio):
        """Process audio data and convert to text"""
        try:
            # Try Google Speech Recognition first
            text = self._recognize_with_google(audio)
            confidence = 0.8  # Google doesn't provide confidence scores
            
            if text:
                self._handle_recognized_text(text, confidence)
                return
            
            # Fallback to other recognition services
            text, confidence = self._recognize_with_fallback(audio)
            if text:
                self._handle_recognized_text(text, confidence)
                
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
    
    def _recognize_with_google(self, audio) -> Optional[str]:
        """Recognize speech using Google Speech Recognition"""
        try:
            text = self.recognizer.recognize_google(
                audio, 
                language=config.LANGUAGE,
                show_all=False
            )
            logger.debug(f"Google recognition result: {text}")
            return text.lower() if text else None
        except sr.UnknownValueError:
            logger.debug("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition: {e}")
            return None
    
    def _recognize_with_fallback(self, audio) -> tuple[Optional[str], float]:
        """Try alternative recognition services"""
        try:
            # Try Sphinx (offline) as fallback
            text = self.recognizer.recognize_sphinx(audio)
            confidence = 0.6  # Lower confidence for offline recognition
            logger.debug(f"Sphinx recognition result: {text}")
            return text.lower() if text else None, confidence
        except sr.UnknownValueError:
            logger.debug("Sphinx could not understand audio")
            return None, 0.0
        except sr.RequestError as e:
            logger.error(f"Sphinx error: {e}")
            return None, 0.0
    
    def _handle_recognized_text(self, text: str, confidence: float):
        """Handle recognized text and call callback if provided"""
        if confidence < config.CONFIDENCE_THRESHOLD:
            logger.debug(f"Low confidence recognition ignored: {text} ({confidence})")
            return
        
        logger.info(f"Recognized: '{text}' (confidence: {confidence})")
        
        # Add to command queue
        self.command_queue.put({
            'text': text,
            'confidence': confidence,
            'timestamp': time.time()
        })
        
        # Call callback if provided
        if self.callback:
            try:
                self.callback(text, confidence)
            except Exception as e:
                logger.error(f"Error in recognition callback: {e}")
    
    def recognize_once(self, timeout: int = 5) -> Optional[Dict[str, Any]]:
        """
        Listen for a single voice command
        
        Args:
            timeout: Maximum time to wait for speech
            
        Returns:
            Dict containing recognized text and confidence, or None
        """
        try:
            with self.microphone as source:
                logger.info("Listening for voice command...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            
            # Try recognition
            text = self._recognize_with_google(audio)
            confidence = 0.8
            
            if not text:
                text, confidence = self._recognize_with_fallback(audio)
            
            if text and confidence >= config.CONFIDENCE_THRESHOLD:
                return {
                    'text': text,
                    'confidence': confidence,
                    'timestamp': time.time()
                }
            
            return None
            
        except sr.WaitTimeoutError:
            logger.info("No speech detected within timeout")
            return None
        except Exception as e:
            logger.error(f"Error during single recognition: {e}")
            return None
    
    def get_command(self, timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        Get the next recognized command from the queue
        
        Args:
            timeout: Maximum time to wait for a command
            
        Returns:
            Dict containing command data, or None if timeout
        """
        try:
            return self.command_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def set_energy_threshold(self, threshold: int):
        """Set the energy threshold for speech detection"""
        self.recognizer.energy_threshold = threshold
        logger.info(f"Energy threshold set to {threshold}")
    
    def get_microphone_list(self) -> list:
        """Get list of available microphones"""
        return sr.Microphone.list_microphone_names()
    
    def test_microphone(self) -> bool:
        """Test if microphone is working"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=1)
            return True
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return False
