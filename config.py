# Environment Configuration for RS Review App
import os

# Determine if we're in production or development
IS_PRODUCTION = os.getenv('RENDER') is not None

# Base URLs for each service
if IS_PRODUCTION:
    # These will be the actual Render URLs once deployed
    SERVICE_URLS = {
        'allothers': os.getenv('ALLOTHERS_URL', 'https://rs-review-main.onrender.com'),
        'interactiveApp': os.getenv('INTERACTIVE1_URL', 'https://rs-review-interactive1.onrender.com'),
        'interactiveApp2': os.getenv('INTERACTIVE2_URL', 'https://rs-review-interactive2.onrender.com'),
        'segmentcountry': os.getenv('SEGMENTCOUNTRY_URL', 'https://rs-review-segmentcountry.onrender.com'),
        'segmentyear': os.getenv('SEGMENTYEAR_URL', 'https://rs-review-segmentyear.onrender.com'),
        'continentsCountries': os.getenv('CONTINENTS_URL', 'https://rs-review-continents.onrender.com'),
        'frontend': os.getenv('FRONTEND_URL', 'https://rs-review-frontend.onrender.com')
    }
else:
    # Local development URLs
    SERVICE_URLS = {
        'allothers': 'http://localhost:8080',
        'interactiveApp': 'http://localhost:8081',
        'interactiveApp2': 'http://localhost:8082',
        'segmentcountry': 'http://localhost:8083',
        'segmentyear': 'http://localhost:8084',
        'continentsCountries': 'http://localhost:8085',
        'frontend': 'http://localhost:3000'
    }

# Port configuration
PORT = int(os.getenv('PORT', 8080))

# Flask configuration
FLASK_CONFIG = {
    'DEBUG': not IS_PRODUCTION,
    'HOST': '0.0.0.0',
    'PORT': PORT
}