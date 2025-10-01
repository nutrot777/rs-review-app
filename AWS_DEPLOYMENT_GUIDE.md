# 🚀 AWS Deployment Guide for RS Review Application

This guide will help you deploy your Recommender Systems Review platform to AWS using App Runner - no cold starts!

## 🎯 **Why AWS App Runner?**

✅ **No Cold Starts** - Services stay warm and responsive  
✅ **Auto-scaling** - Handles traffic spikes  
✅ **Free Tier Friendly** - Fits within student allowance  
✅ **Simple Setup** - Deploy directly from GitHub  
✅ **Better Performance** - Faster than Render free tier  

## 📋 **Prerequisites**

- [x] AWS Account with student free tier
- [x] GitHub repository (you have this)
- [x] AWS CLI installed (optional but helpful)

## 🚀 **Step-by-Step Deployment**

### **Step 1: Access AWS App Runner**

1. **Login to AWS Console**: https://console.aws.amazon.com
2. **Search for "App Runner"** in the services search
3. **Click "Create service"**

### **Step 2: Deploy Main Service (Flask App)**

**Service 1: Main Flask App**
1. **Source**: GitHub repository
2. **Repository**: `nutrot777/rs-review-app`
3. **Branch**: `main`
4. **Configuration**: Use configuration file
5. **Configuration file**: `apprunner-main.yaml`
6. **Service name**: `rs-review-main`
7. **Click "Create & Deploy"**

### **Step 3: Deploy Interactive Services**

Repeat for each service with these configuration files:

| Service | Config File | Purpose |
|---------|-------------|---------|
| rs-review-interactive1 | `apprunner-interactive1.yaml` | Years & Countries |
| rs-review-interactive2 | Create new config | Years, Segments & Countries |
| rs-review-segmentcountry | Create new config | Segments & Countries |
| rs-review-segmentyear | Create new config | Years & Segments |
| rs-review-continents | Create new config | Continents & Countries |
| rs-review-frontend | `apprunner-frontend.yaml` | Frontend |

### **Step 4: Get Service URLs**

After deployment, each service will have a URL like:
- `https://XXXXXXXXX.us-east-1.awsapprunner.com`

### **Step 5: Update Frontend URLs**

Update `update_urls_for_production.py` with the new AWS URLs.

## 💰 **Cost Estimation (Free Tier)**

**App Runner Free Tier:**
- **Build time**: 100 build minutes/month (FREE)
- **Compute**: 2 GB RAM, 1 vCPU hours/month (FREE)
- **Additional**: $0.064/GB RAM per hour, $0.032/vCPU per hour

**Your 7 services estimated monthly cost**: ~$15-25/month after free tier
**Within student budget**: Very reasonable for academic project

## 🔄 **Migration from Render**

1. **Keep Render running** during AWS setup
2. **Deploy to AWS** following this guide
3. **Test AWS deployment** thoroughly
4. **Update DNS/URLs** to point to AWS
5. **Decommission Render** services

## ⚡ **Performance Benefits**

**AWS App Runner vs Render Free:**
- ❌ **No cold starts** (vs 30-60s on Render)
- ⚡ **Faster downloads** (better infrastructure)
- 🔄 **Auto-scaling** (handles traffic spikes)
- 📊 **Better monitoring** (CloudWatch integration)
- 🛡️ **More reliable** (AWS infrastructure)

## 🛠️ **Troubleshooting**

**Build Failures**: Check requirements.txt and Python version  
**Service Errors**: View logs in App Runner console  
**URL Issues**: Update production URL script  
**High Costs**: Monitor usage in AWS billing dashboard  

---

**Ready to start?** Let me know and I'll help you create the remaining configuration files and guide you through the AWS console setup!