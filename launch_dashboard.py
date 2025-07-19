#!/usr/bin/env python3
import subprocess
import time
import socket
import webbrowser
import os
import sys

def check_port(host, port):
    """Check if a port is available"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def find_available_port(start_port=8080):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + 100):
        if not check_port('127.0.0.1', port):
            return port
    return None

def launch_streamlit(port):
    """Launch Streamlit dashboard"""
    try:
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 'dashboard.py',
            '--server.port', str(port),
            '--server.address', '127.0.0.1',
            '--server.headless', 'true',
            '--server.enableCORS', 'false',
            '--server.enableXsrfProtection', 'false',
            '--server.runOnSave', 'false'
        ]
        
        # Add local bin to PATH
        env = os.environ.copy()
        env['PATH'] = '/home/ubuntu/.local/bin:' + env.get('PATH', '')
        
        process = subprocess.Popen(cmd, env=env)
        return process, port
    except Exception as e:
        print(f"Error launching Streamlit: {e}")
        return None, None

def main():
    print("🚀 Customer Segmentation Dashboard Launcher")
    print("=" * 50)
    
    # Find available port
    port = find_available_port(8080)
    if not port:
        print("❌ No available ports found!")
        return
    
    print(f"🔍 Using port: {port}")
    
    # Launch Streamlit
    process, used_port = launch_streamlit(port)
    if not process:
        print("❌ Failed to launch Streamlit")
        return
    
    print("⏳ Starting dashboard...")
    time.sleep(5)
    
    # Check if it's running
    if check_port('127.0.0.1', used_port):
        print("✅ Dashboard is running!")
        
        urls = [
            f"http://localhost:{used_port}",
            f"http://127.0.0.1:{used_port}"
        ]
        
        print("\n🌐 Access your dashboard at:")
        for i, url in enumerate(urls, 1):
            print(f"   {i}. {url}")
        
        print(f"\n📋 Copy this URL: http://localhost:{used_port}")
        print("\n🎯 Features available:")
        print("   • Interactive RFM analysis")
        print("   • 3D customer visualization")
        print("   • Segment filtering")
        print("   • Business insights")
        print("   • Data export")
        
        print(f"\n🔄 To stop: Press Ctrl+C or kill process {process.pid}")
        
        # Try to open browser
        try:
            webbrowser.open(f"http://localhost:{used_port}")
            print("🌐 Attempting to open browser...")
        except:
            pass
        
        # Keep running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping dashboard...")
            process.terminate()
    else:
        print("❌ Dashboard failed to start")
        process.terminate()

if __name__ == "__main__":
    main()