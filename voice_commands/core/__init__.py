"""
Voice Commands Core Module

This module provides the core functionality for voice recognition and command processing
in the ManVue fashion e-commerce application.
"""

from .voice_recognizer import VoiceRecognizer
from .command_processor import CommandProcessor
from .text_to_speech import TextToSpeech

__version__ = "1.0.0"
__author__ = "ManVue Development Team"

__all__ = [
    "VoiceRecognizer",
    "CommandProcessor", 
    "TextToSpeech"
]
