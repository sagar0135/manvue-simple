"""
Voice Commands API Integration for ManVue Application

This module provides API endpoints for voice command functionality.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
import logging
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from ..core.voice_recognizer import VoiceRecognizer
from ..core.command_processor import CommandProcessor
from ..core.text_to_speech import TextToSpeech
from ..config.voice_config import config

logger = logging.getLogger(__name__)

# Create router for voice endpoints
voice_router = APIRouter(prefix="/api/voice", tags=["voice"])

# Global instances
voice_recognizer = None
command_processor = None
tts_engine = None
active_connections: Dict[str, WebSocket] = {}

class ConnectionManager:
    """Manages WebSocket connections for voice commands"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.user_sessions[session_id] = {
            'connected_at': datetime.now(),
            'commands_processed': 0,
            'last_activity': datetime.now()
        }
        logger.info(f"Voice WebSocket connected: {session_id}")
    
    def disconnect(self, session_id: str):
        """Remove WebSocket connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.user_sessions:
            del self.user_sessions[session_id]
        logger.info(f"Voice WebSocket disconnected: {session_id}")
    
    async def send_personal_message(self, message: dict, session_id: str):
        """Send message to specific connection"""
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
                self.user_sessions[session_id]['last_activity'] = datetime.now()
            except Exception as e:
                logger.error(f"Error sending message to {session_id}: {e}")
                self.disconnect(session_id)
    
    async def broadcast(self, message: dict):
        """Send message to all connections"""
        disconnected = []
        for session_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception:
                disconnected.append(session_id)
        
        # Clean up disconnected clients
        for session_id in disconnected:
            self.disconnect(session_id)

manager = ConnectionManager()

def init_voice_services():
    """Initialize voice recognition services"""
    global voice_recognizer, command_processor, tts_engine
    
    try:
        command_processor = CommandProcessor()
        tts_engine = TextToSpeech()
        
        # Register action handlers
        register_action_handlers()
        
        logger.info("Voice services initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize voice services: {e}")
        return False

def register_action_handlers():
    """Register handlers for voice commands"""
    global command_processor
    
    if not command_processor:
        return
    
    async def handle_search_products(action_data):
        """Handle product search commands"""
        query = action_data['parameters'].get('query', '')
        logger.info(f"Voice search: {query}")
        
        # Here you would integrate with your product search API
        # For now, return a mock response
        return {
            'action': 'search_executed',
            'query': query,
            'results_count': 42  # Mock result
        }
    
    async def handle_navigation(action_data):
        """Handle navigation commands"""
        page = action_data['parameters'].get('page', '')
        url = action_data['parameters'].get('url', '')
        logger.info(f"Voice navigation: {page} -> {url}")
        
        return {
            'action': 'navigation_executed',
            'page': page,
            'url': url
        }
    
    async def handle_cart_actions(action_data):
        """Handle cart-related commands"""
        logger.info("Voice cart action executed")
        
        return {
            'action': 'cart_action_executed'
        }
    
    # Register handlers
    command_processor.register_action_handler('search_products', handle_search_products)
    command_processor.register_action_handler('navigate_to_page', handle_navigation)
    command_processor.register_action_handler('open_cart', handle_cart_actions)
    command_processor.register_action_handler('add_to_cart', handle_cart_actions)

@voice_router.on_event("startup")
async def startup_voice_services():
    """Initialize voice services on startup"""
    init_voice_services()

@voice_router.get("/status")
async def get_voice_status():
    """Get voice services status"""
    return {
        'voice_recognition_available': voice_recognizer is not None,
        'command_processor_available': command_processor is not None,
        'tts_available': tts_engine is not None,
        'active_connections': len(manager.active_connections),
        'config': {
            'language': config.LANGUAGE,
            'confidence_threshold': config.CONFIDENCE_THRESHOLD,
            'features_enabled': config.FEATURES
        }
    }

@voice_router.get("/commands")
async def get_available_commands():
    """Get list of available voice commands"""
    if not command_processor:
        raise HTTPException(status_code=503, detail="Command processor not available")
    
    try:
        commands = command_processor.get_available_commands()
        return {
            'commands': commands,
            'total_count': len(commands),
            'categories': list(command_processor.commands_config.get('voice_commands', {}).keys())
        }
    except Exception as e:
        logger.error(f"Error getting commands: {e}")
        raise HTTPException(status_code=500, detail="Failed to get commands")

@voice_router.post("/process")
async def process_voice_command(command_data: dict):
    """Process a voice command"""
    if not command_processor:
        raise HTTPException(status_code=503, detail="Command processor not available")
    
    try:
        text = command_data.get('text', '')
        confidence = command_data.get('confidence', 0.8)
        
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        result = command_processor.process_command(text, confidence)
        
        if result:
            return {
                'success': True,
                'result': result,
                'processed_at': datetime.now().isoformat()
            }
        else:
            return {
                'success': False,
                'message': 'No matching command found',
                'processed_at': datetime.now().isoformat()
            }
    
    except Exception as e:
        logger.error(f"Error processing command: {e}")
        raise HTTPException(status_code=500, detail="Failed to process command")

@voice_router.post("/speak")
async def text_to_speech(speech_data: dict):
    """Convert text to speech"""
    if not tts_engine or not tts_engine.is_enabled():
        raise HTTPException(status_code=503, detail="Text-to-speech not available")
    
    try:
        text = speech_data.get('text', '')
        priority = speech_data.get('priority', 0)
        interrupt = speech_data.get('interrupt', False)
        
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        tts_engine.speak(text, priority, interrupt)
        
        return {
            'success': True,
            'message': 'Speech queued',
            'text': text,
            'queued_at': datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error in text-to-speech: {e}")
        raise HTTPException(status_code=500, detail="Failed to process speech")

@voice_router.websocket("/ws/{session_id}")
async def voice_websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time voice communication"""
    await manager.connect(websocket, session_id)
    
    try:
        # Send welcome message
        await manager.send_personal_message({
            'type': 'connection_established',
            'session_id': session_id,
            'features': config.FEATURES,
            'timestamp': datetime.now().isoformat()
        }, session_id)
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            await handle_websocket_message(message, session_id)
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"WebSocket error for {session_id}: {e}")
        manager.disconnect(session_id)

async def handle_websocket_message(message: dict, session_id: str):
    """Handle incoming WebSocket messages"""
    message_type = message.get('type')
    
    try:
        if message_type == 'voice_command':
            # Process voice command
            text = message.get('text', '')
            confidence = message.get('confidence', 0.8)
            
            if command_processor and text:
                result = command_processor.process_command(text, confidence)
                
                response = {
                    'type': 'command_result',
                    'original_text': text,
                    'result': result,
                    'timestamp': datetime.now().isoformat()
                }
                
                await manager.send_personal_message(response, session_id)
                
                # Update session stats
                if session_id in manager.user_sessions:
                    manager.user_sessions[session_id]['commands_processed'] += 1
        
        elif message_type == 'start_listening':
            # Start voice recognition (if available)
            response = {
                'type': 'listening_started',
                'timestamp': datetime.now().isoformat()
            }
            await manager.send_personal_message(response, session_id)
        
        elif message_type == 'stop_listening':
            # Stop voice recognition
            response = {
                'type': 'listening_stopped',
                'timestamp': datetime.now().isoformat()
            }
            await manager.send_personal_message(response, session_id)
        
        elif message_type == 'get_commands':
            # Send available commands
            if command_processor:
                commands = command_processor.get_available_commands()
                response = {
                    'type': 'available_commands',
                    'commands': commands,
                    'timestamp': datetime.now().isoformat()
                }
                await manager.send_personal_message(response, session_id)
        
        elif message_type == 'ping':
            # Heartbeat
            response = {
                'type': 'pong',
                'timestamp': datetime.now().isoformat()
            }
            await manager.send_personal_message(response, session_id)
        
        else:
            # Unknown message type
            response = {
                'type': 'error',
                'message': f'Unknown message type: {message_type}',
                'timestamp': datetime.now().isoformat()
            }
            await manager.send_personal_message(response, session_id)
    
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}")
        error_response = {
            'type': 'error',
            'message': 'Failed to process message',
            'timestamp': datetime.now().isoformat()
        }
        await manager.send_personal_message(error_response, session_id)

@voice_router.get("/sessions")
async def get_active_sessions():
    """Get information about active voice sessions"""
    sessions = []
    for session_id, session_data in manager.user_sessions.items():
        sessions.append({
            'session_id': session_id,
            'connected_at': session_data['connected_at'].isoformat(),
            'commands_processed': session_data['commands_processed'],
            'last_activity': session_data['last_activity'].isoformat()
        })
    
    return {
        'active_sessions': sessions,
        'total_sessions': len(sessions)
    }

@voice_router.post("/shutdown")
async def shutdown_voice_services():
    """Shutdown voice services"""
    global voice_recognizer, command_processor, tts_engine
    
    try:
        # Disconnect all WebSocket connections
        for session_id in list(manager.active_connections.keys()):
            await manager.send_personal_message({
                'type': 'service_shutdown',
                'message': 'Voice services are shutting down',
                'timestamp': datetime.now().isoformat()
            }, session_id)
            manager.disconnect(session_id)
        
        # Shutdown services
        if tts_engine:
            tts_engine.shutdown()
        
        voice_recognizer = None
        command_processor = None
        tts_engine = None
        
        return {'success': True, 'message': 'Voice services shutdown completed'}
    
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        raise HTTPException(status_code=500, detail="Failed to shutdown services")

# Include the router in your main FastAPI app:
# app.include_router(voice_router)
