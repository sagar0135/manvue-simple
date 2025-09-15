#!/usr/bin/env python3
"""
Simple ManVue System Startup
Starts only the frontend server without complex dependencies
"""

import subprocess
import sys
import time
import webbrowser
import threading
from pathlib import Path

def start_simple_server():
    """Start a simple HTTP server for the frontend"""
    print("🌐 Starting Frontend Server...")
    try:
        # Use Python's built-in HTTP server
        process = subprocess.Popen([
            sys.executable, "-m", "http.server", "3000"
        ], cwd="frontend")
        
        print("✅ Frontend Server started on http://localhost:3000")
        return process
    except Exception as e:
        print(f"❌ Failed to start Frontend Server: {e}")
        return None

def open_browser():
    """Open browser after a delay"""
    def delayed_open():
        time.sleep(2)
        try:
            webbrowser.open("http://localhost:3000")
            print("🌐 Opening browser...")
        except Exception as e:
            print(f"❌ Failed to open browser: {e}")
    
    thread = threading.Thread(target=delayed_open)
    thread.daemon = True
    thread.start()

def main():
    """Main function"""
    print("🚀 Starting ManVue Simple System...")
    print("=" * 40)
    
    try:
        # Start frontend server
        server_process = start_simple_server()
        
        if server_process:
            # Open browser
            open_browser()
            
            print("\n" + "=" * 40)
            print("🎉 ManVue System Started!")
            print("=" * 40)
            print("📱 Website: http://localhost:3000")
            print("=" * 40)
            print("Press Ctrl+C to stop the server")
            
            # Wait for the process
            server_process.wait()
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user")
        if 'server_process' in locals() and server_process:
            server_process.terminate()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
