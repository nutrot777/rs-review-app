#!/usr/bin/env python3
"""
Simple HTTP server for serving static HTML files on Render
"""

import os
import http.server
import socketserver
from pathlib import Path
import subprocess

# Update URLs for production
def update_urls():
    """Run the URL update script"""
    try:
        subprocess.run(['python', 'update_urls_for_production.py'], check=True)
        print("URLs updated for production")
    except subprocess.CalledProcessError:
        print("Warning: Could not update URLs")

# Custom handler to serve HTML files
class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='frontend', **kwargs)
    
    def do_GET(self):
        # If requesting root, serve homepage.html
        if self.path == '/' or self.path == '':
            self.path = '/homepage.html'
        super().do_GET()

if __name__ == "__main__":
    # Update URLs first
    update_urls()
    
    # Get port from environment
    PORT = int(os.environ.get('PORT', 3000))
    
    # Create server
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving frontend at port {PORT}")
        httpd.serve_forever()