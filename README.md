# Recommender Systems Review - Interactive Dashboard

A comprehensive web application showcasing systematic review findings on recommender systems research. This application presents interactive visualizations for exploring publications across different dimensions: People, Process, and Technology.

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Applications Overview](#-applications-overview)
- [Local Development](#-local-development)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)

## 🚀 Quick Start

### 1. Set Up Unified Environment
```bash
python install_dependencies.py
```
This creates a single virtual environment and installs all dependencies (solves macOS "externally managed environment" issue).

### 2. Run All Applications
```bash
python run_all.py
```

### 3. Access the Dashboard
Open your browser and go to: **http://localhost:3000**

That's it! All 7 applications will be running simultaneously in an isolated environment.

## 📁 Project Structure

```
rs-review-app/
├── README.md                    # This file
├── run_all.py                   # Master startup script
├── install_dependencies.py     # Dependency installer
├── frontend/                    # Static HTML dashboard
│   ├── homepage.html           # Main landing page
│   ├── rsfinding1.html         # Venn diagram visualization
│   ├── rsfinding2.html         # Years & Countries sunburst
│   ├── rsfinding3.html         # Segments & Countries treemap
│   ├── rsfinding4.html         # Years & Segments stacked chart
│   ├── rsfinding5.html         # Years, Segments & Countries sunburst
│   ├── themes_in_abstract.html # Extracted themes data
│   ├── paperscitations.html    # Reference citations
│   └── sources/                # Images and assets
├── backend/                     # Flask/Dash applications
│   ├── allothers/              # Themes & References (Flask)
│   ├── interactiveApp/         # Years & Countries (Dash)
│   ├── interactiveApp2/        # Years, Segments & Countries (Dash)
│   ├── segmentcountry/         # Segments & Countries (Dash)
│   ├── segmentyear/            # Years & Segments (Dash)
│   └── continentsCountries/    # Continents & Countries (Dash)
└── scripts/                     # Utility scripts
    └── prepare_deployment.py   # Deployment helper
```

## 🎯 Applications Overview

| Application | Port | Type | Description | Features |
|-------------|------|------|-------------|----------|
| **Homepage** | 3000 | Static | Main dashboard | Navigation, overview cards |
| **allothers** | 8080 | Flask | Themes & References | Data tables, citations, themes |
| **interactiveApp** | 8081 | Dash | Years & Countries | Sunburst chart, modal details |
| **interactiveApp2** | 8082 | Dash | Years, Segments & Countries | Multi-level sunburst |
| **segmentcountry** | 8083 | Dash | Segments & Countries | Treemap visualization |
| **segmentyear** | 8084 | Dash | Years & Segments | Stacked area chart |
| **continentsCountries** | 8085 | Dash | Continents & Countries | Interactive bubble chart |

## 💻 Local Development

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step-by-Step Setup

1. **Navigate to the project directory**:
   ```bash
   cd rs-review-app
   ```

2. **Set up unified virtual environment** (one-time setup):
   ```bash
   python install_dependencies.py
   ```
   This creates a `venv/` directory with all dependencies isolated from your system Python.

3. **Verify setup** (optional):
   ```bash
   python verify_setup.py
   ```

4. **Start all applications**:
   ```bash
   python run_all.py
   ```

5. **Access the application**:
   - Main Dashboard: http://localhost:3000
   - Individual apps: http://localhost:8080-8085

### Individual App Testing

To test a specific backend app:
```bash
cd backend/[app_name]
python app.py
```

### Stopping Applications

Press `Ctrl+C` in the terminal running `run_all.py` to stop all applications gracefully.

## 🌍 Deployment

### Option 1: Railway (Recommended)

Railway offers easy deployment with generous free tier:

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy each backend app**:
   ```bash
   cd backend/allothers
   railway login
   railway init
   railway up
   ```

3. **Repeat for all 6 backend apps**

4. **Deploy frontend** to Netlify/Vercel (static hosting)

5. **Update HTML files** with deployed URLs

### Option 2: Docker Deployment

1. **Create deployment configs**:
   ```bash
   python scripts/prepare_deployment.py
   ```

2. **Build and run**:
   ```bash
   cd deployment/docker
   docker-compose up --build
   ```

### Option 3: Other Platforms

**Backend Apps** can be deployed to:
- Heroku
- Render
- DigitalOcean App Platform
- PythonAnywhere

**Frontend** can be deployed to:
- Netlify
- Vercel
- GitHub Pages
- Any static hosting service

## 🔧 Configuration

### Port Configuration

Default ports are defined in `run_all.py`. To change ports:

1. Edit the `APPS` dictionary in `run_all.py`
2. Update corresponding HTML iframe URLs in frontend files

### Data Source

All applications fetch data from:
```
https://raw.githubusercontent.com/trial777/combined_selected_RS/main/combined_selected_v3.xlsx
```

To use a different data source, update the `url` variable in each backend app's `app.py` file.

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**:
```bash
# Check what's using the port
lsof -i :8080

# Kill the process
kill -9 [PID]
```

**Dependencies Not Installing**:
```bash
# Install manually
cd backend/[app_name]
pip install -r requirements.txt
```

**HTML Pages Not Loading Backend Data**:
1. Ensure all backend apps are running
2. Check browser console for CORS errors
3. Verify URLs in HTML files match running applications

**Application Won't Start**:
1. Check Python version: `python --version`
2. Verify all dependencies are installed
3. Check for typos in file paths
4. Review error messages in terminal

### Getting Help

If you encounter issues:

1. **Check the terminal output** for error messages
2. **Verify all ports are available** (3000, 8080-8085)
3. **Ensure Python 3.8+** is installed
4. **Check network connectivity** for data fetching

## 📊 Data & Research

This application visualizes systematic review data on recommender systems research, analyzing publications across three key dimensions:

- **People**: Human factors, user experience, social aspects
- **Process**: Methodologies, algorithms, workflows
- **Technology**: Technical implementations, platforms, tools

### Key Visualizations

1. **Three-Way Venn Diagram**: Shows overlap between People, Process, Technology dimensions
2. **Sunburst Charts**: Interactive exploration of Years → Countries → Segments
3. **Treemap**: Hierarchical view of Segments → Countries
4. **Stacked Charts**: Temporal analysis of segment evolution
5. **Data Tables**: Detailed publication metadata and extracted themes

## 📝 Citation

If you use this application or data in your research, please cite:

```
[Your Citation Information Here]
```

## 🤝 Contributing

This is a research project. For questions or collaboration opportunities, please contact the research team.

---

**🎉 Enjoy exploring the recommender systems research landscape!**