#!/usr/bin/env python3
"""
ManVue Chatbot Integration Server
Connects Rasa chatbot with ManVue API and provides WebSocket interface
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import asyncio
import json
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional
import uvicorn
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
RASA_SERVER_URL = "http://localhost:5005"
MANVUE_API_URL = "http://localhost:5000"
CHATBOT_PORT = 5055

app = FastAPI(
    title="ManVue Chatbot Server",
    description="Integration server for ManVue Fashion Chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
frontend_path = Path(__file__).parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Connection manager for WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"Client {session_id} connected")
        
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"Client {session_id} disconnected")
            
    async def send_message(self, message: str, session_id: str):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_text(message)

manager = ConnectionManager()

class ManVueChatbotIntegration:
    def __init__(self):
        self.rasa_url = RASA_SERVER_URL
        self.manvue_api_url = MANVUE_API_URL
        
    async def send_to_rasa(self, message: str, sender: str) -> List[Dict]:
        """Send message to Rasa and get response"""
        try:
            payload = {
                "sender": sender,
                "message": message
            }
            
            # Try to connect to Rasa server
            async with asyncio.timeout(5):
                response = requests.post(
                    f"{self.rasa_url}/webhooks/rest/webhook",
                    json=payload,
                    timeout=5
                )
                
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Rasa server error: {response.status_code}")
                return self.get_fallback_response(message)
                
        except Exception as e:
            logger.error(f"Error connecting to Rasa: {e}")
            return self.get_fallback_response(message)
    
    def get_fallback_response(self, message: str) -> List[Dict]:
        """Provide fallback responses when Rasa is unavailable"""
        message_lower = message.lower()
        
        # Simple keyword-based responses
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greet']):
            return [{
                "text": "👋 Hello! Welcome to ManVue! I'm your fashion assistant. How can I help you today?\n\n🛍️ I can help you with:\n• Product searches\n• Size guides\n• Shipping information\n• Return policies\n• Current deals"
            }]
        elif any(word in message_lower for word in ['product', 'search', 'find', 'show']):
            return [{
                "text": "🔍 I can help you find products! Try searching for:\n• T-shirts\n• Shirts\n• Jackets\n• Bottoms\n• Accessories\n\nWhat type of item are you looking for?"
            }]
        elif any(word in message_lower for word in ['size', 'sizing', 'measurement']):
            return [{
                "text": "📏 **Size Guide:**\n• XS: 32-34\" chest\n• S: 34-36\" chest\n• M: 36-38\" chest\n• L: 38-40\" chest\n• XL: 40-42\" chest\n• XXL: 42-44\" chest\n\nNeed help with specific sizing?"
            }]
        elif any(word in message_lower for word in ['shipping', 'delivery', 'ship']):
            return [{
                "text": "🚚 **Shipping Information:**\n• Free shipping on orders over $75\n• Standard delivery: 3-5 business days\n• Express delivery: 1-2 business days\n• International shipping available\n\nNeed tracking information?"
            }]
        elif any(word in message_lower for word in ['return', 'refund', 'exchange']):
            return [{
                "text": "🔄 **Return Policy:**\n• 30-day return window\n• Items must be unworn with tags\n• Free returns on defective items\n• Easy online return process\n\nNeed help with a return?"
            }]
        elif any(word in message_lower for word in ['deal', 'sale', 'discount', 'offer']):
            return [{
                "text": "🔥 **Current Deals:**\n• 20% off Winter Collection\n• Buy 2 Get 1 Free on T-Shirts\n• Free shipping on orders $75+\n• Student discount: 15% off\n\nCheck our website for the latest offers!"
            }]
        elif any(word in message_lower for word in ['bye', 'goodbye', 'thanks', 'thank you']):
            return [{
                "text": "Thank you for chatting with ManVue! 👔✨\n\nHave a stylish day and don't forget to check out our latest arrivals!"
            }]
        else:
            return [{
                "text": "🤔 I'm here to help! I can assist you with:\n\n🛍️ **Shopping:**\n• Product searches\n• Size guides\n• Recommendations\n\n📦 **Orders:**\n• Shipping info\n• Return policy\n• Tracking\n\n💡 **Support:**\n• Contact info\n• Store locations\n• Current deals\n\nWhat would you like to know more about?"
            }]
    
    async def get_manvue_products(self, query: str = None, category: str = None) -> Dict:
        """Get products from ManVue API"""
        try:
            params = {}
            if query:
                params['search'] = query
            if category:
                params['category'] = category
                
            response = requests.get(
                f"{self.manvue_api_url}/products",
                params=params,
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Unable to fetch products"}
                
        except Exception as e:
            logger.error(f"Error fetching ManVue products: {e}")
            return {"error": "Service temporarily unavailable"}

chatbot = ManVueChatbotIntegration()

@app.get("/")
async def read_root():
    """Serve the chatbot interface"""
    try:
        frontend_file = frontend_path / "chatbot.html"
        if frontend_file.exists():
            return FileResponse(frontend_file)
        else:
            return HTMLResponse("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>ManVue Chatbot Server</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    .status { color: #27ae60; font-weight: bold; }
                    .error { color: #e74c3c; }
                    .endpoint { background: #ecf0f1; padding: 10px; border-radius: 5px; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🤖 ManVue Chatbot Server</h1>
                    <p class="status">✅ Server is running successfully!</p>
                    
                    <h3>Available Endpoints:</h3>
                    <div class="endpoint"><strong>WebSocket:</strong> ws://localhost:5055/ws</div>
                    <div class="endpoint"><strong>HTTP API:</strong> http://localhost:5055/chat</div>
                    <div class="endpoint"><strong>Health Check:</strong> http://localhost:5055/health</div>
                    
                    <h3>Integration Status:</h3>
                    <p>✅ Chatbot server active</p>
                    <p>🔄 Frontend files: <span class="error">Not found (check /frontend directory)</span></p>
                    
                    <h3>To use the chatbot:</h3>
                    <ol>
                        <li>Ensure Rasa server is running on port 5005</li>
                        <li>Include the chatbot widget in your ManVue frontend</li>
                        <li>Connect to WebSocket endpoint for real-time chat</li>
                    </ol>
                </div>
            </body>
            </html>
            """)
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "chatbot_server": "running",
            "rasa_server": await check_rasa_connection(),
            "manvue_api": await check_manvue_connection()
        }
    }

async def check_rasa_connection():
    """Check if Rasa server is accessible"""
    try:
        response = requests.get(f"{RASA_SERVER_URL}/status", timeout=3)
        return "connected" if response.status_code == 200 else "disconnected"
    except:
        return "disconnected"

async def check_manvue_connection():
    """Check if ManVue API is accessible"""
    try:
        response = requests.get(f"{MANVUE_API_URL}/", timeout=3)
        return "connected" if response.status_code == 200 else "disconnected"
    except:
        return "disconnected"

@app.post("/chat")
async def chat_endpoint(request: dict):
    """HTTP endpoint for chat messages"""
    message = request.get("message", "")
    sender = request.get("sender", "user")
    
    if not message:
        return {"error": "Message is required"}
    
    try:
        responses = await chatbot.send_to_rasa(message, sender)
        return {"responses": responses}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {"error": "Failed to process message"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    session_id = f"ws_{datetime.now().timestamp()}"
    
    try:
        await manager.connect(websocket, session_id)
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
                message = message_data.get("message", "")
                sender = message_data.get("sender", session_id)
                
                if message:
                    # Send to Rasa and get response
                    responses = await chatbot.send_to_rasa(message, sender)
                    
                    # Send responses back to client
                    await manager.send_message(
                        json.dumps(responses),
                        session_id
                    )
                    
            except json.JSONDecodeError:
                # Handle plain text messages
                responses = await chatbot.send_to_rasa(data, session_id)
                await manager.send_message(
                    json.dumps(responses),
                    session_id
                )
                
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(session_id)

@app.get("/products")
async def get_products(query: str = None, category: str = None):
    """Proxy endpoint for ManVue products"""
    return await chatbot.get_manvue_products(query, category)

if __name__ == "__main__":
    print("🚀 Starting ManVue Chatbot Server...")
    print(f"📱 Frontend: http://localhost:{CHATBOT_PORT}")
    print(f"🔌 WebSocket: ws://localhost:{CHATBOT_PORT}/ws")
    print(f"🌐 API: http://localhost:{CHATBOT_PORT}/chat")
    print("👋 Ready to chat!")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=CHATBOT_PORT,
        log_level="info"
    )

