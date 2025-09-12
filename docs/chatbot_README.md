# 🤖 ManVue Fashion Chatbot

An intelligent, responsive chatbot integrated with the ManVue fashion e-commerce platform. Built with Rasa framework and featuring modern UI/UX design.

## ✨ Features

### 🎯 Smart Assistance
- **Product Search**: AI-powered product discovery and recommendations
- **Size Guide**: Interactive sizing help and measurements
- **Order Support**: Tracking, returns, and customer service
- **Fashion Advice**: Style recommendations and trends

### 🎨 Modern Interface
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Voice Input**: Speech-to-text functionality
- **Real-time Chat**: WebSocket-powered instant messaging
- **Quick Actions**: One-click common queries
- **Typing Indicators**: Enhanced user experience

### 🔧 Technical Features
- **Rasa Framework**: Advanced NLP and conversation management
- **FastAPI Integration**: High-performance API connectivity
- **WebSocket Support**: Real-time bidirectional communication
- **Fallback Handling**: Graceful degradation when services are unavailable
- **Analytics Ready**: Built-in event tracking

## 🚀 Quick Start

### Option 1: One-Command Startup (Recommended)

#### Windows
```bash
cd chatbot
start_chatbot.bat
```

#### Linux/Mac
```bash
cd chatbot
chmod +x start_chatbot.sh
./start_chatbot.sh
```

#### Python
```bash
cd chatbot
python start_chatbot.py
```

### Option 2: Manual Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Train the Model**
```bash
rasa train
```

3. **Start Services**
```bash
# Terminal 1: Rasa Server
rasa run --enable-api --cors "*" --port 5005

# Terminal 2: Action Server
rasa run actions --port 5055

# Terminal 3: Integration Server
python chatbot_server.py
```

## 📁 Project Structure

```
chatbot/
├── 🤖 Rasa Configuration
│   ├── config.yml              # Rasa pipeline configuration
│   ├── domain.yml              # Intents, entities, responses
│   ├── credentials.yml         # Channel configurations
│   └── endpoints.yml           # Service endpoints
├── 📚 Training Data
│   ├── data/
│   │   ├── nlu.yml            # Natural language understanding
│   │   ├── stories.yml        # Conversation flows
│   │   └── rules.yml          # Conversation rules
├── 🎬 Custom Actions
│   ├── actions/
│   │   ├── __init__.py
│   │   └── actions.py         # Custom chatbot actions
├── 🎨 Frontend Interface
│   ├── frontend/
│   │   ├── chatbot.html       # Chatbot UI
│   │   ├── chatbot.css        # Responsive styles
│   │   └── chatbot.js         # Interactive functionality
├── 🔧 Integration
│   ├── chatbot_server.py      # FastAPI integration server
│   ├── chatbot_widget.js      # Easy integration widget
│   └── start_chatbot.py       # Unified startup script
├── 🚀 Startup Scripts
│   ├── start_chatbot.bat      # Windows startup
│   ├── start_chatbot.sh       # Unix/Linux/Mac startup
│   └── requirements.txt       # Python dependencies
└── 📖 Documentation
    └── README.md              # This file
```

## 🎯 Integration with ManVue

### Method 1: Automatic Integration (Recommended)

Add to your ManVue HTML pages:

```html
<!-- Add this before closing </body> tag -->
<div data-manvue-chatbot 
     data-chatbot-server="http://localhost:5055"
     data-chatbot-position="bottom-right"
     data-chatbot-theme="manvue">
</div>
<script src="http://localhost:5055/static/chatbot_widget.js"></script>
```

### Method 2: Manual Integration

```html
<!-- Include the widget -->
<script src="chatbot/chatbot_widget.js"></script>
<script>
// Initialize chatbot
const chatbot = ManVueChatbotWidget.init({
    serverUrl: 'http://localhost:5055',
    websocketUrl: 'ws://localhost:5055/ws',
    position: 'bottom-right',
    enableVoice: true,
    showWelcome: true
});
</script>
```

### Method 3: Direct Iframe

```html
<iframe 
    src="http://localhost:5055" 
    width="400" 
    height="600"
    style="border:none; border-radius:10px;">
</iframe>
```

## 🔧 Configuration

### Environment Setup

Create a `.env` file (optional):
```ini
# Chatbot Configuration
RASA_SERVER_URL=http://localhost:5005
MANVUE_API_URL=http://localhost:5000
CHATBOT_PORT=5055

# Logging
LOG_LEVEL=INFO

# Features
ENABLE_VOICE=true
ENABLE_ANALYTICS=true
```

### Customization

Edit `domain.yml` to add new intents and responses:
```yaml
intents:
  - your_custom_intent

responses:
  utter_custom_response:
  - text: "Your custom response here"
```

Add training data in `data/nlu.yml`:
```yaml
- intent: your_custom_intent
  examples: |
    - your example phrase
    - another example
```

## 🛠️ API Endpoints

### Chatbot Server (Port 5055)
- `GET /` - Chatbot interface
- `GET /health` - Health check
- `POST /chat` - HTTP chat endpoint
- `WebSocket /ws` - Real-time chat
- `GET /static/*` - Static files

### Rasa Server (Port 5005)
- `POST /webhooks/rest/webhook` - Chat messages
- `GET /status` - Server status
- `GET /conversations/{id}/tracker` - Conversation tracking

### Action Server (Port 5055)
- `POST /webhook` - Custom actions
- Integration with ManVue API

## 🎨 Customization

### Styling

Edit `frontend/chatbot.css` for custom themes:

```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
    /* Add your brand colors */
}
```

### Responses

Modify responses in `domain.yml`:

```yaml
responses:
  utter_greet:
  - text: "Welcome to [Your Brand]! How can I help?"
```

### Actions

Add custom logic in `actions/actions.py`:

```python
class YourCustomAction(Action):
    def name(self) -> Text:
        return "action_your_custom_action"
    
    def run(self, dispatcher, tracker, domain):
        # Your custom logic here
        return []
```

## 📊 Analytics & Monitoring

### Built-in Events
- `chatbot_opened` - When user opens chat
- `message_sent` - When user sends message
- `message_received` - When bot responds
- `action_clicked` - When quick action is used

### Integration with Analytics

```javascript
// Google Analytics
window.gtag('event', 'chatbot_interaction', {
    'event_category': 'chatbot',
    'event_label': 'message_sent'
});

// Custom analytics
window.manvueChatbotWidget.on('message_sent', (data) => {
    // Your analytics code
});
```

## 🔧 Troubleshooting

### Common Issues

1. **Chatbot not responding**
   - Check if Rasa server is running: `http://localhost:5005/status`
   - Verify action server is running on port 5055
   - Check browser console for errors

2. **Voice input not working**
   - Ensure HTTPS or localhost (required for speech recognition)
   - Check browser permissions for microphone
   - Verify browser supports Speech Recognition API

3. **Widget not appearing**
   - Check if chatbot_widget.js is loaded correctly
   - Verify server is running on correct port
   - Check browser console for JavaScript errors

4. **Styling issues**
   - Ensure CSS files are loaded
   - Check for CSS conflicts with main site
   - Verify correct z-index values

### Debug Mode

Enable debug logging:
```bash
python start_chatbot.py --debug
```

View logs:
```bash
# Rasa logs
rasa run --debug

# Action server logs
rasa run actions --debug
```

## 🚀 Deployment

### Development
```bash
python start_chatbot.py
```

### Production

1. **Configure Environment**
```bash
export RASA_SERVER_URL=https://your-rasa-server.com
export MANVUE_API_URL=https://your-api.com
```

2. **Use Production Server**
```bash
gunicorn chatbot_server:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. **Docker Deployment**
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "start_chatbot.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

### Development Setup
```bash
# Clone and setup
git clone <your-repo>
cd chatbot
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Train and test
rasa train
rasa test
```

## 📄 License

This project is part of the ManVue platform and follows the same licensing terms.

## 🆘 Support

- 📧 Email: support@manvue.com
- 💬 Chat: Use the chatbot on our website
- 📚 Docs: [ManVue Documentation](https://docs.manvue.com)
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)

---

**Built with ❤️ for ManVue Fashion Platform**

