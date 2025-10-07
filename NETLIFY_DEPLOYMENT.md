# Complete Netlify Deployment Guide - IAEF

## 🎯 Overview

This guide provides step-by-step instructions for deploying the Inegben Adaptive EdTech Framework (IAEF) to Netlify. The application consists of a React frontend and FastAPI backend adapted for Netlify Functions.

## 🏗️ Architecture

### Frontend (Static Site)
- **Framework**: React 18 with Create React App
- **Build**: Standard `npm run build` output
- **Hosting**: Netlify Static Site Hosting
- **Routing**: Client-side routing with React Router

### Backend (Serverless Functions)
- **Framework**: FastAPI adapted for Netlify Functions
- **Runtime**: Python 3.8+ via Netlify Functions
- **Database**: PostgreSQL (external service)
- **Authentication**: JWT tokens

## 📋 Prerequisites

1. **Netlify Account**: Sign up at [netlify.com](https://netlify.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Database**: Set up a PostgreSQL database (recommended: Supabase, PlanetScale, or Railway)
4. **Python 3.8+**: For local development and testing

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

1. **Ensure all Netlify files are committed**:
   ```bash
   git add .
   git commit -m "Add Netlify deployment configuration"
   git push origin main
   ```

### Step 2: Connect to Netlify

1. **Go to Netlify Dashboard**:
   - Visit [app.netlify.com](https://app.netlify.com)
   - Click "New site from Git"

2. **Connect GitHub Repository**:
   - Choose "GitHub" as your Git provider
   - Select your IAEF repository
   - Authorize Netlify to access your repository

### Step 3: Configure Build Settings

**Build Configuration**:
- **Base directory**: `frontend`
- **Build command**: `npm run build`
- **Publish directory**: `frontend/build`
- **Node version**: `18` (set in Environment Variables)

### Step 4: Set Environment Variables

Go to **Site Settings → Environment Variables** and add:

#### Frontend Environment Variables
| Variable | Value | Environment |
|----------|-------|-------------|
| `REACT_APP_API_URL` | `https://your-site-name.netlify.app` | Production, Preview, Development |

#### Backend Environment Variables (for Functions)
| Variable | Value | Environment |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://user:pass@host:port/db` | Production, Preview, Development |
| `SECRET_KEY` | `your-256-bit-secret-key-here` | Production, Preview, Development |
| `ALGORITHM` | `HS256` | Production, Preview, Development |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Production, Preview, Development |
| `NETLIFY_SITE_URL` | `https://your-site-name.netlify.app` | Production, Preview, Development |

### Step 5: Deploy

1. **Click "Deploy site"**
2. **Monitor the build process** in the Netlify dashboard
3. **Check function logs** if there are any issues

## 🗄️ Database Setup

### Option 1: Supabase (Recommended)
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings → Database
4. Copy the connection string
5. Add to `DATABASE_URL` environment variable

### Option 2: PlanetScale (MySQL)
1. Go to [planetscale.com](https://planetscale.com)
2. Create a new database
3. Copy the connection string
4. Add to `DATABASE_URL` environment variable

### Option 3: Railway
1. Go to [railway.app](https://railway.app)
2. Create a new PostgreSQL service
3. Copy the connection string
4. Add to `DATABASE_URL` environment variable

## 🔧 Configuration Files

### `netlify.toml` (Root)
```toml
[build]
  base = "frontend"
  publish = "frontend/build"
  command = "npm run build"

[build.environment]
  NODE_VERSION = "18"
  NPM_VERSION = "9"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### `netlify/functions/api.py`
- FastAPI app wrapped with Mangum for Netlify Functions
- Handles all API routes under `/api/*`

### `netlify/functions/requirements.txt`
- Python dependencies for Netlify Functions
- Optimized for serverless environment

## 🐛 Troubleshooting

### Common Issues

#### 1. Function Timeout
**Error**: Function execution timeout
**Solution**: 
- Optimize database queries
- Add connection pooling
- Consider caching strategies

#### 2. CORS Errors
**Error**: CORS policy blocks requests
**Solution**: 
- Update `ALLOWED_ORIGINS` in environment variables
- Check `netlify.toml` redirects configuration

#### 3. Database Connection Issues
**Error**: Database connection failed
**Solution**: 
- Verify `DATABASE_URL` format
- Check database credentials
- Ensure database allows external connections

#### 4. Build Failures
**Error**: Frontend build fails
**Solution**: 
- Check Node.js version (should be 18)
- Verify all dependencies are installed
- Check for TypeScript/ESLint errors

#### 5. Function Not Found
**Error**: 404 for API endpoints
**Solution**: 
- Verify `netlify.toml` redirects
- Check function file structure
- Ensure `api.py` is in `netlify/functions/`

### Debugging Steps

1. **Check Build Logs**:
   - Go to Site → Deploys
   - Click on the latest deploy
   - Review build logs for errors

2. **Check Function Logs**:
   - Go to Site → Functions
   - Click on function name
   - Review execution logs

3. **Test Locally**:
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli
   
   # Start local development
   netlify dev
   ```

## 🚀 Testing Your Deployment

### Frontend Test
Visit: `https://your-site-name.netlify.app`

### Backend API Test
```bash
# Health check
curl https://your-site-name.netlify.app/api/health

# API info
curl https://your-site-name.netlify.app/api/
```

### Function Test
```bash
# Test function directly
curl https://your-site-name.netlify.app/.netlify/functions/api/
```

## 📊 Monitoring

1. **Netlify Analytics**: Enable in site settings
2. **Function Logs**: Monitor in Netlify dashboard
3. **Error Tracking**: Consider Sentry integration
4. **Performance**: Use Netlify's built-in performance monitoring

## 🔄 Continuous Deployment

- **Automatic deploys** on Git push to main branch
- **Preview deployments** for pull requests
- **Branch deploys** for feature branches
- **Environment-specific** configurations

## 🆘 Support

### Netlify Resources
- [Netlify Functions Documentation](https://docs.netlify.com/functions/overview/)
- [Netlify Build Configuration](https://docs.netlify.com/configure-builds/overview/)
- [Netlify Environment Variables](https://docs.netlify.com/environment-variables/overview/)

### Common Commands
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy to Netlify
netlify deploy

# Deploy with production URL
netlify deploy --prod
```

---

**Your IAEF application should now be successfully deployed on Netlify!** 🎉

The combination of static site hosting for the frontend and serverless functions for the backend provides excellent performance and scalability.
