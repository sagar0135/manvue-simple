# Voice Commands Module

This module provides voice command functionality for the ManVue fashion e-commerce application.

## Features

- **Voice Recognition**: Convert speech to text using Web Speech API and Python speech recognition
- **Voice Commands**: Process natural language commands for navigation and actions
- **Text-to-Speech**: Provide audio feedback to users
- **Voice Search**: Search products using voice input
- **Accessibility**: Improve accessibility for users with visual impairments

## Directory Structure

```
voice_commands/
├── README.md                 # This file
├── config/
│   ├── voice_config.py      # Voice recognition configuration
│   └── commands_config.json # Voice command mappings
├── core/
│   ├── __init__.py
│   ├── voice_recognizer.py  # Main voice recognition class
│   ├── command_processor.py # Process and execute voice commands
│   └── text_to_speech.py    # Text-to-speech functionality
├── frontend/
│   ├── voice_interface.js   # Frontend voice interface
│   ├── voice_ui.js          # Voice UI components
│   └── voice_commands.css   # Voice-related styling
├── integration/
│   ├── api_integration.py   # Backend voice API endpoints
│   └── ml_voice_integration.py # ML model voice integration
├── examples/
│   ├── basic_usage.html     # Basic voice command examples
│   └── advanced_usage.py    # Advanced Python usage examples
└── requirements.txt         # Voice module dependencies
```

## Quick Start

### Frontend Integration
```html
<script src="voice_commands/frontend/voice_interface.js"></script>
<script>
    const voiceInterface = new VoiceInterface();
    voiceInterface.startListening();
</script>
```

### Backend Integration
```python
from voice_commands.core.voice_recognizer import VoiceRecognizer
from voice_commands.core.command_processor import CommandProcessor

recognizer = VoiceRecognizer()
processor = CommandProcessor()
```

## Voice Commands

### Navigation Commands
- "Go to home page"
- "Show products"
- "Open cart"
- "View profile"

### Search Commands
- "Search for [product name]"
- "Find [category] items"
- "Show me [color] [item type]"

### Product Commands
- "Add to cart"
- "Show product details"
- "Compare products"
- "Filter by [criteria]"

### Accessibility Commands
- "Read page content"
- "Describe image"
- "Navigate to next item"

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r voice_commands/requirements.txt
   ```

2. Include frontend scripts in your HTML:
   ```html
   <script src="voice_commands/frontend/voice_interface.js"></script>
   <link rel="stylesheet" href="voice_commands/frontend/voice_commands.css">
   ```

## Browser Support

- Chrome 25+
- Firefox 44+
- Safari 14.1+
- Edge 79+

## Configuration

Voice recognition and command processing can be configured through:
- `config/voice_config.py` - Python configuration
- `config/commands_config.json` - Command mappings

## Privacy

This module processes voice data locally when possible. External services are only used when specified in configuration.
