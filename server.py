#!/usr/bin/env python3
"""
Development Server for Static Site Generator
Serves the built site content on localhost:1313
"""

import os
import sys
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
from urllib.parse import urlparse


class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Only log important messages
        if args and len(args) > 1:
            status_code = args[1]
            if status_code.startswith('2'):  # 2xx success
                return  # Don't log successful requests
        
        # For other requests (errors, etc.), use simplified logging
        print(f"[{self.address_string()}] {format % args}")
    
    def do_GET(self):
        #Override to handle missing files gracefully during rebuilds
        
        try:
            super().do_GET()
        except (FileNotFoundError, OSError, PermissionError):
            # If file not found during rebuild, send a temporary response
            print("Build in progress, serving rebuild page...")
            self.send_response(503)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Refresh', '2')  # Auto-refresh in 2 seconds
            self.end_headers()
            rebuild_html = '''<!DOCTYPE html>
<html><head><title>Site Rebuilding</title></head>
<body style="font-family: 'JetBrains Mono', monospace; text-align: center; padding: 50px; background: #000; color: #f5f5dc;">
    <h2>🔄 Site Rebuilding...</h2>
    <p>The site is being rebuilt. This page will refresh automatically.</p>
    <script>setTimeout(() => location.reload(), 2000);</script>
</body></html>'''
            self.wfile.write(rebuild_html.encode('utf-8'))


class StaticSiteServer:
    def __init__(self, port=1313, build_dir="build"):
        self.port = port
        self.build_dir = Path(build_dir)
        self.server = None
    
    def check_build_dir(self):
        if not self.build_dir.exists():
            print(f"Build directory '{self.build_dir}' not found!")
            print("Please run 'python builder.py' first to build the site.")
            return False
        
        if not self.build_dir.is_dir():
            print(f"'{self.build_dir}' exists but is not a directory!")
            return False
        
        # Check if there's an index.html in the build directory
        index_file = self.build_dir / "index.html"
        if not index_file.exists():
            print(f"No index.html found in '{self.build_dir}'")
            print("The site might not have a homepage.")
        
        return True
    
    def start_server(self, open_browser=True):
        if not self.check_build_dir():
            return False
        
        # Change to build directory
        original_cwd = os.getcwd()
        os.chdir(self.build_dir)
        
        try:
            # Create server
            self.server = HTTPServer(('localhost', self.port), QuietHTTPRequestHandler)
            server_url = f"http://localhost:{self.port}"
            
            print(f"Starting development server...")
            print(f"Serving files from: {self.build_dir.absolute()}")
            print(f"Server running at: {server_url}")
            print(f"Press Ctrl+C to stop the server")
            
            # Open browser if requested
            if open_browser:
                print(f"🔗 Opening browser...")
                webbrowser.open(server_url)
            
            # Start serving
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print(f"\nServer stopped by user")
            return True
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f"Port {self.port} is already in use!")
                print(f"Try using a different port or stop the other server.")
            else:
                print(f"Error starting server: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
            if self.server:
                self.server.server_close()
    
    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("Server stopped")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Serve static site for development')
    parser.add_argument('--port', '-p', type=int, default=1313, 
                        help='Port to serve on (default: 1313)')
    parser.add_argument('--build-dir', '-d', default='build',
                        help='Build directory to serve (default: build)')
    parser.add_argument('--no-browser', action='store_true',
                        help="Don't automatically open browser")
    
    args = parser.parse_args()
    
    # Create and start server
    server = StaticSiteServer(port=args.port, build_dir=args.build_dir)
    success = server.start_server(open_browser=not args.no_browser)
    
    sys.exit(0 if success else 1)
