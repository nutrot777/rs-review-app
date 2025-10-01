#!/usr/bin/env python3
"""
Helper script to prepare applications for deployment.
Creates deployment configurations for various platforms.
"""

import json
from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).parent

def create_railway_configs():
    """Create Railway deployment configurations"""
    railway_dir = BASE_DIR / "deployment" / "railway"
    railway_dir.mkdir(parents=True, exist_ok=True)
    
    apps = {
        "allothers": {"port": 8080, "name": "rs-themes-references"},
        "interactiveApp": {"port": 8081, "name": "rs-years-countries"},
        "interactiveApp2": {"port": 8082, "name": "rs-years-segments-countries"},
        "segmentcountry": {"port": 8083, "name": "rs-segments-countries"},
        "segmentyear": {"port": 8084, "name": "rs-years-segments"},
        "continentsCountries": {"port": 8085, "name": "rs-continents-countries"}
    }
    
    for app_name, config in apps.items():
        # Create railway.json for each app
        railway_config = {
            "build": {
                "builder": "NIXPACKS"
            },
            "deploy": {
                "startCommand": "python app.py",
                "healthcheckPath": "/",
                "healthcheckTimeout": 300,
                "restartPolicyType": "ON_FAILURE",
                "restartPolicyMaxRetries": 10
            }
        }
        
        config_file = railway_dir / f"{app_name}-railway.json"
        with open(config_file, 'w') as f:
            json.dump(railway_config, f, indent=2)
    
    print("✅ Created Railway configurations")

def create_docker_configs():
    """Create Docker configurations for all apps"""
    docker_dir = BASE_DIR / "deployment" / "docker"
    docker_dir.mkdir(parents=True, exist_ok=True)
    
    # Create docker-compose.yml
    compose_config = {
        "version": "3.8",
        "services": {
            "homepage": {
                "build": {
                    "context": "./frontend",
                    "dockerfile": "Dockerfile"
                },
                "ports": ["3000:3000"],
                "depends_on": ["allothers", "interactiveapp", "interactiveapp2", "segmentcountry", "segmentyear", "continentscountries"]
            },
            "allothers": {
                "build": {
                    "context": "./backend/allothers",
                    "dockerfile": "Dockerfile"
                },
                "ports": ["8080:8080"],
                "environment": ["PORT=8080"]
            },
            "interactiveapp": {
                "build": {
                    "context": "./backend/interactiveApp",
                    "dockerfile": "Dockerfile"
                },
                "ports": ["8081:8081"],
                "environment": ["PORT=8081"]
            },
            "interactiveapp2": {
                "build": {
                    "context": "./backend/interactiveApp2",
                    "dockerfile": "Dockerfile"
                },
                "ports": ["8082:8082"],
                "environment": ["PORT=8082"]
            },
            "segmentcountry": {
                "build": {
                    "context": "./backend/segmentcountry",
                    "dockerfile": "Dockerfile"
                },
                "ports": ["8083:8083"],
                "environment": ["PORT=8083"]
            },
            "segmentyear": {
                "build": {
                    "context": "./backend/segmentyear",
                    "dockerfile": "Dockerfile"
                },
                "ports": ["8084:8084"],
                "environment": ["PORT=8084"]
            },
            "continentscountries": {
                "build": {
                    "context": "./backend/continentsCountries",
                    "dockerfile": "Dockerfile"
                },
                "ports": ["8085:8085"],
                "environment": ["PORT=8085"]
            }
        }
    }
    
    # Save docker-compose.yml
    import yaml
    try:
        with open(docker_dir / "docker-compose.yml", 'w') as f:
            yaml.dump(compose_config, f, default_flow_style=False)
        print("✅ Created Docker Compose configuration")
    except ImportError:
        print("⚠️  PyYAML not installed. Creating JSON version instead.")
        with open(docker_dir / "docker-compose.json", 'w') as f:
            json.dump(compose_config, f, indent=2)

def create_frontend_dockerfile():
    """Create Dockerfile for frontend"""
    dockerfile_content = '''FROM python:3.9-slim

WORKDIR /app

# Copy frontend files
COPY . /app

# Create a simple server script
RUN echo 'import http.server\\n\\
import socketserver\\n\\
PORT = 3000\\n\\
Handler = http.server.SimpleHTTPRequestHandler\\n\\
with socketserver.TCPServer(("", PORT), Handler) as httpd:\\n\\
    print(f"Server running at http://localhost:{PORT}")\\n\\
    httpd.serve_forever()' > server.py

EXPOSE 3000

CMD ["python", "server.py"]
'''
    
    frontend_dockerfile = BASE_DIR / "frontend" / "Dockerfile"
    with open(frontend_dockerfile, 'w') as f:
        f.write(dockerfile_content)
    
    print("✅ Created frontend Dockerfile")

def create_deployment_readme():
    """Create deployment instructions"""
    readme_content = '''# Deployment Guide

## Railway Deployment (Recommended)

1. **Create Railway account**: https://railway.app
2. **Deploy each backend app separately**:
   ```bash
   # For each app in backend/
   cd backend/[app_name]
   railway login
   railway init
   railway up
   ```
3. **Get deployed URLs** and update frontend HTML files
4. **Deploy frontend** to Netlify/Vercel (static hosting)

## Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   cd deployment/docker
   docker-compose up --build
   ```

## Manual Deployment Steps

### Backend Apps (Flask/Dash)
Each backend app can be deployed to:
- Railway
- Heroku
- Render
- DigitalOcean App Platform

### Frontend (Static HTML)
Deploy to:
- Netlify
- Vercel
- GitHub Pages
- Any static hosting service

## Environment Variables

Each backend app uses:
- `PORT`: Server port (set automatically by most platforms)

## URL Updates

After deploying backend apps, update frontend HTML files:
1. Replace `http://localhost:XXXX` with deployed URLs
2. Update iframe src attributes in HTML files
'''
    
    deployment_dir = BASE_DIR / "deployment"
    deployment_dir.mkdir(exist_ok=True)
    
    with open(deployment_dir / "README.md", 'w') as f:
        f.write(readme_content)
    
    print("✅ Created deployment README")

def main():
    """Main function to create deployment configurations"""
    print("🚀 Creating Deployment Configurations")
    print("=" * 50)
    
    create_railway_configs()
    create_docker_configs()
    create_frontend_dockerfile()
    create_deployment_readme()
    
    print("=" * 50)
    print("✅ All deployment configurations created!")
    print("📁 Check the 'deployment' directory for configuration files")

if __name__ == "__main__":
    main()