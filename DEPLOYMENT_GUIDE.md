# 🚀 RS Review Application - Render Deployment Guide

This guide will help you deploy your Recommender Systems Review visualization platform to Render.com.

## 📋 Pre-Deployment Checklist

✅ All applications use environment variables for ports  
✅ URL update script created for production  
✅ render.yaml configuration file ready  
✅ Requirements.txt includes all dependencies  

## 🎯 Deployment Steps

### Step 1: Prepare GitHub Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Render deployment"
   ```

2. **Create GitHub Repository**:
   - Go to [GitHub.com](https://github.com)
   - Click "New Repository"
   - Name it: `rs-review-visualization`
   - Make it Public (required for Render free tier)
   - Don't initialize with README (we already have files)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/rs-review-visualization.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Render

1. **Create Render Account**:
   - Go to [render.com](https://render.com)
   - Sign up with GitHub account

2. **Deploy Services**:
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository: `rs-review-visualization`
   - Render will automatically detect the `render.yaml` file
   - Click "Apply" to create all services

### Step 3: Configure Service URLs

After deployment, you'll get these URLs (update the `update_urls_for_production.py` with actual URLs):

- Frontend: `https://rs-review-frontend.onrender.com`
- Main App: `https://rs-review-main.onrender.com`
- Interactive 1: `https://rs-review-interactive1.onrender.com`
- Interactive 2: `https://rs-review-interactive2.onrender.com`
- Segment Country: `https://rs-review-segmentcountry.onrender.com`
- Segment Year: `https://rs-review-segmentyear.onrender.com`
- Continents: `https://rs-review-continents.onrender.com`

## 🔧 Service Configuration

Each service will be configured with:
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Port**: 10000 (Render's default)
- **Health Check**: Automatic

## 📊 Expected Services

| Service | Purpose | Port | URL Pattern |
|---------|---------|------|-------------|
| rs-review-frontend | Static HTML files | - | `*.onrender.com` |
| rs-review-main | Themes & References | 10000 | `rs-review-main.onrender.com` |
| rs-review-interactive1 | Years & Countries | 10000 | `rs-review-interactive1.onrender.com` |
| rs-review-interactive2 | Years, Segments & Countries | 10000 | `rs-review-interactive2.onrender.com` |
| rs-review-segmentcountry | Segments & Countries | 10000 | `rs-review-segmentcountry.onrender.com` |
| rs-review-segmentyear | Years & Segments | 10000 | `rs-review-segmentyear.onrender.com` |
| rs-review-continents | Continents & Countries | 10000 | `rs-review-continents.onrender.com` |

## ⏱️ Deployment Timeline

- **Initial Build**: 5-10 minutes per service
- **Total Deployment**: ~30-45 minutes for all services
- **Cold Start**: Services sleep after 15 min of inactivity (free tier)
- **Wake Up Time**: 30-60 seconds when accessing sleeping service

## 🎉 Post-Deployment

1. **Test All Services**: Visit each URL to ensure they're working
2. **Update URLs**: If service names differ, update `update_urls_for_production.py`
3. **Monitor Logs**: Check Render dashboard for any errors
4. **Share**: Your main URL will be the frontend service URL

## 🔍 Troubleshooting

**Build Failures**: Check requirements.txt for any missing dependencies  
**Service Errors**: Review logs in Render dashboard  
**URL Issues**: Ensure all localhost URLs are updated in HTML files  
**Cold Starts**: First visit after inactivity takes longer  

## 💡 Tips

- Services on free tier sleep after 15 minutes of inactivity
- Each service can handle ~100 concurrent users
- Consider upgrading to paid plans for production use
- Monitor usage in Render dashboard

---

**Need Help?** Check the Render dashboard logs or contact support through their platform.