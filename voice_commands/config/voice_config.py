"""
Voice Recognition Configuration for ManVue Application
"""

import os
from typing import Dict, List, Optional

class VoiceConfig:
    """Configuration class for voice recognition settings"""
    
    # Speech Recognition Settings
    RECOGNITION_TIMEOUT = 5  # seconds to wait for speech
    PHRASE_TIMEOUT = 1      # seconds of silence to consider phrase complete
    ENERGY_THRESHOLD = 4000  # microphone sensitivity threshold
    
    # Language Settings
    LANGUAGE = "en-US"  # Primary language for recognition
    FALLBACK_LANGUAGES = ["en-GB", "en-CA", "en-AU"]
    
    # Voice Engine Settings
    TTS_ENGINE = "pyttsx3"  # Text-to-speech engine
    TTS_RATE = 200         # Speech rate (words per minute)
    TTS_VOLUME = 0.8       # Volume level (0.0 to 1.0)
    
    # Command Processing
    CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence for command execution
    MAX_COMMAND_RETRIES = 3     # Maximum retries for failed commands
    
    # Web Speech API Settings (Frontend)
    WEB_SPEECH_CONTINUOUS = True
    WEB_SPEECH_INTERIM_RESULTS = True
    WEB_SPEECH_MAX_ALTERNATIVES = 3
    
    # Audio Settings
    SAMPLE_RATE = 16000    # Audio sample rate in Hz
    CHUNK_SIZE = 1024      # Audio chunk size for processing
    
    # Hotword Detection
    HOTWORDS = ["hey manvue", "manvue", "voice command"]
    HOTWORD_SENSITIVITY = 0.5
    
    # API Settings
    VOICE_API_ENDPOINT = "/api/voice"
    VOICE_WEBSOCKET_ENDPOINT = "/ws/voice"
    
    # File Paths
    AUDIO_TEMP_DIR = os.path.join(os.path.dirname(__file__), "..", "temp")
    MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
    
    # Features Toggle
    FEATURES = {
        "voice_search": True,
        "voice_navigation": True,
        "text_to_speech": True,
        "voice_accessibility": True,
        "voice_cart_management": True,
        "voice_product_info": True
    }
    
    # Debug Settings
    DEBUG_MODE = False
    LOG_VOICE_COMMANDS = True
    SAVE_AUDIO_SAMPLES = False

    @classmethod
    def get_feature_config(cls, feature: str) -> bool:
        """Check if a voice feature is enabled"""
        return cls.FEATURES.get(feature, False)
    
    @classmethod
    def update_config(cls, **kwargs):
        """Update configuration values"""
        for key, value in kwargs.items():
            if hasattr(cls, key.upper()):
                setattr(cls, key.upper(), value)
    
    @classmethod
    def get_supported_languages(cls) -> List[str]:
        """Get list of supported languages"""
        return [cls.LANGUAGE] + cls.FALLBACK_LANGUAGES

# Environment-specific configurations
class DevelopmentConfig(VoiceConfig):
    DEBUG_MODE = True
    LOG_VOICE_COMMANDS = True
    SAVE_AUDIO_SAMPLES = True

class ProductionConfig(VoiceConfig):
    DEBUG_MODE = False
    LOG_VOICE_COMMANDS = False
    SAVE_AUDIO_SAMPLES = False
    CONFIDENCE_THRESHOLD = 0.8

class TestingConfig(VoiceConfig):
    RECOGNITION_TIMEOUT = 2
    MAX_COMMAND_RETRIES = 1
    DEBUG_MODE = True

# Select configuration based on environment
ENV = os.getenv('ENVIRONMENT', 'development').lower()

if ENV == 'production':
    config = ProductionConfig
elif ENV == 'testing':
    config = TestingConfig
else:
    config = DevelopmentConfig
