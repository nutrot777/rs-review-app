#!/bin/bash

# Start all services in background
echo "Starting RS Review Applications..."

# Start Flask apps
cd /app/backend/allothers && python app.py &
cd /app/backend/segmentcountry && python app.py &
cd /app/backend/segmentyear && python app.py &
cd /app/backend/interactiveApp && python app.py &
cd /app/backend/interactiveApp2 && python app.py &
cd /app/backend/continentsCountries && python app.py &

# Start static file server for frontend
cd /app/frontend && python -m http.server 3000 &

# Wait for all background processes
wait