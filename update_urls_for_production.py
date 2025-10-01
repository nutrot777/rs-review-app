#!/usr/bin/env python3
"""
Update HTML files to use production URLs instead of localhost
This script runs during the build process on Render
"""

import os
import re
from pathlib import Path

# Production URLs (actual Render service URLs)
PRODUCTION_URLS = {
    'http://localhost:8080': 'https://rs-review-main.onrender.com',
    'http://localhost:8081': 'https://rs-review-interactive1.onrender.com', 
    'http://localhost:8082': 'https://rs-review-interactive2.onrender.com',
    'http://localhost:8083': 'https://rs-review-segmentcountry.onrender.com',
    'http://localhost:8084': 'https://rs-review-segmentyear.onrender.com',
    'http://localhost:8085': 'https://rs-review-continents.onrender.com',
    'http://localhost:3000': 'https://rs-review-frontend.onrender.com'
}

def update_html_files():
    """Update all HTML files in the frontend directory"""
    frontend_dir = Path('frontend')
    
    if not frontend_dir.exists():
        print("Frontend directory not found")
        return
    
    # Get all HTML files
    html_files = list(frontend_dir.glob('*.html'))
    
    print(f"Found {len(html_files)} HTML files to update")
    
    for html_file in html_files:
        print(f"Updating {html_file}...")
        
        # Read the file
        content = html_file.read_text(encoding='utf-8')
        
        # Replace all localhost URLs
        for localhost_url, production_url in PRODUCTION_URLS.items():
            if localhost_url in content:
                content = content.replace(localhost_url, production_url)
                print(f"  Replaced {localhost_url} with {production_url}")
        
        # Write back the updated content
        html_file.write_text(content, encoding='utf-8')
    
    print("URL updates completed!")

if __name__ == '__main__':
    # Only run if we're in production (Render sets this)
    if os.getenv('RENDER'):
        update_html_files()
    else:
        print("Running in development mode - no URL updates needed")