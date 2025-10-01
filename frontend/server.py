
import http.server
import socketserver
import os
from pathlib import Path

PORT = int(os.environ.get('PORT', 3000))
DIRECTORY = Path(__file__).parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        # If requesting root path, serve homepage.html
        if self.path == '/' or self.path == '':
            self.path = '/homepage.html'
        super().do_GET()
    
    def end_headers(self):
        # Add CORS headers to allow iframe embedding
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

if __name__ == "__main__":
    # Use 0.0.0.0 for AWS deployment, localhost for local development
    host = "0.0.0.0" if os.environ.get('AWS_DEPLOYMENT') else "localhost"
    with socketserver.TCPServer((host, PORT), Handler) as httpd:
        print(f"🏠 Homepage server running at http://{host}:{PORT}")
        print(f"📁 Serving files from: {DIRECTORY}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Homepage server stopped.")
