# Vercel Deployment Guide for IAEF

This guide explains how to deploy the Inegben Adaptive EdTech Framework (IAEF) to Vercel.

## 🏗️ Architecture Overview

The IAEF project consists of two main components:
- **Backend**: FastAPI application (Python)
- **Frontend**: React application (Node.js)

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Database**: Set up a PostgreSQL database (recommended: Vercel Postgres, Supabase, or PlanetScale)

## 🚀 Deployment Steps

**Recommended Approach**: Deploy frontend and backend as separate Vercel projects for better performance and easier management.

### Step 1: Backend Deployment

1. **Connect Repository to Vercel**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Backend Project**:
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements-vercel.txt`
   - **Output Directory**: Leave empty (serverless function)

3. **Environment Variables Setup**:
   
   **Step-by-Step Instructions:**
   
   a) **Navigate to Project Settings**:
      - Go to your Vercel project dashboard
      - Click on the "Settings" tab
      - Select "Environment Variables" from the left sidebar
   
   b) **Add Each Environment Variable**:
      Click "Add New" for each variable below:
      
      | Variable Name | Value | Environment |
      |---------------|-------|-------------|
      | `DATABASE_URL` | `postgresql://username:password@host:port/database` | Production, Preview, Development |
      | `SECRET_KEY` | `your-super-secret-key-here` | Production, Preview, Development |
      | `ALGORITHM` | `HS256` | Production, Preview, Development |
      | `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Production, Preview, Development |
      | `ALLOWED_ORIGINS` | `https://your-frontend-domain.vercel.app` | Production, Preview, Development |
   
   c) **Important Notes**:
      - ✅ **DO**: Set these as regular environment variables
      - ❌ **DON'T**: Use the "Secrets" section or `@variable` syntax
      - 🔒 **Security**: Use strong, unique values for `SECRET_KEY`
      - 🌍 **Environments**: Enable for Production, Preview, and Development
   
   d) **Database URL Examples**:
      ```
      # Vercel Postgres
      postgres://default:password@ep-xxx.us-east-1.postgres.vercel-storage.com/verceldb
      
      # Supabase
      postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
      
      # PlanetScale
      mysql://username:password@aws.connect.psdb.cloud/database?sslaccept=strict
      ```

4. **Deploy Backend**:
   - Click "Deploy"
   - Note the deployment URL (e.g., `https://iaef-backend.vercel.app`)

### Step 2: Frontend Deployment

1. **Create New Vercel Project**:
   - Go to Vercel Dashboard
   - Click "New Project"
   - Import the same GitHub repository

2. **Configure Frontend Project**:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install` (optional, auto-detected)

3. **Environment Variables Setup**:
   
   **Step-by-Step Instructions:**
   
   a) **Navigate to Project Settings**:
      - Go to your Vercel project dashboard
      - Click on the "Settings" tab
      - Select "Environment Variables" from the left sidebar
   
   b) **Add Environment Variable**:
      Click "Add New" and enter:
      
      | Variable Name | Value | Environment |
      |---------------|-------|-------------|
      | `REACT_APP_API_URL` | `https://iaef-backend.vercel.app` | Production, Preview, Development |
   
   c) **Important Notes**:
      - ✅ **DO**: Set as regular environment variable
      - ❌ **DON'T**: Use secrets or `@variable` syntax
      - 🔄 **Update**: Replace with your actual backend URL after deployment
      - 🌍 **Environments**: Enable for all environments

4. **Deploy Frontend**:
   - Click "Deploy"
   - Note the deployment URL (e.g., `https://iaef-frontend.vercel.app`)

### Step 3: Update CORS Configuration

1. **Update Backend CORS**:
   - Go to your backend project in Vercel
   - Update the `ALLOWED_ORIGINS` environment variable:
   ```
   ALLOWED_ORIGINS=https://iaef-frontend.vercel.app,https://your-custom-domain.com
   ```
   - Redeploy the backend

## 🔧 Configuration Files

### Backend Configuration (`backend/vercel.json`)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb",
        "maxDuration": 30
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ],
  "env": {
    "PYTHONPATH": ".",
    "DATABASE_URL": "@database_url",
    "SECRET_KEY": "@secret_key",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
    "ALLOWED_ORIGINS": "https://your-frontend-domain.vercel.app,http://localhost:3000"
  }
}
```

### Frontend Configuration (`frontend/vercel.json`)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "REACT_APP_API_URL": "@api_url"
  }
}
```

## 🗄️ Database Setup

### Option 1: Vercel Postgres (Recommended)
1. Go to your Vercel project dashboard
2. Click on "Storage" tab
3. Create a new Postgres database
4. Copy the connection string to `DATABASE_URL`

### Option 2: External Database
- **Supabase**: Free tier available, easy setup
- **PlanetScale**: MySQL-compatible, serverless
- **Railway**: PostgreSQL hosting

## 🔐 Security Considerations

1. **Environment Variables**:
   - ✅ **DO**: Use Vercel's environment variable system
   - ✅ **DO**: Set strong, unique values for `SECRET_KEY`
   - ✅ **DO**: Enable variables for appropriate environments only
   - ❌ **DON'T**: Commit secrets to Git
   - ❌ **DON'T**: Use the same secrets across projects
   - ❌ **DON'T**: Use `@variable` syntax (causes deployment errors)

2. **Environment Variable Best Practices**:
   ```
   # ✅ CORRECT: Regular environment variables
   DATABASE_URL = postgresql://user:pass@host:port/db
   SECRET_KEY = your-256-bit-secret-key-here
   
   # ❌ WRONG: Secret references (causes errors)
   DATABASE_URL = @database_url
   SECRET_KEY = @secret_key
   ```

3. **CORS Configuration**:
   - Only allow your frontend domain
   - Remove localhost origins in production
   - Use exact URLs, not wildcards

4. **Database Security**:
   - Use connection pooling
   - Enable SSL connections
   - Regular backups
   - Rotate database credentials regularly

## 🐛 Troubleshooting

### Common Issues

1. **Environment Variable Errors**:
   - ❌ **Error**: "Secret does not exist" or "Environment Variable references Secret"
   - ✅ **Solution**: Use regular environment variables, NOT secrets
   - ❌ **Error**: `@database_url` or `@secret_key` syntax errors
   - ✅ **Solution**: Remove `@` prefix, use direct values
   - ❌ **Error**: Variables not available in function
   - ✅ **Solution**: Ensure variables are enabled for Production, Preview, and Development

2. **Build Failures**:
   - Check Python version compatibility
   - Verify all dependencies in `requirements-vercel.txt`
   - Check build logs in Vercel dashboard
   - Ensure environment variables are set before build

3. **CORS Errors**:
   - Verify `ALLOWED_ORIGINS` includes your frontend URL
   - Check browser developer tools for specific errors
   - Ensure no trailing slashes in URLs

4. **Database Connection Issues**:
   - Verify `DATABASE_URL` format and credentials
   - Check database accessibility from Vercel
   - Ensure SSL is enabled if required
   - Test connection string locally first

5. **Function Timeout**:
   - Increase `maxDuration` in `vercel.json`
   - Optimize database queries
   - Consider caching strategies

6. **Authentication Issues**:
   - Verify `SECRET_KEY` is set and strong
   - Check JWT token expiration settings
   - Ensure `ALGORITHM` matches your code

### Debugging Steps

1. **Check Vercel Logs**:
   - Go to project dashboard
   - Click on "Functions" tab
   - View real-time logs

2. **Test API Endpoints**:
   ```bash
   curl https://your-backend.vercel.app/health
   curl https://your-backend.vercel.app/api/v1/users/me
   ```

3. **Frontend Debugging**:
   - Check browser console for errors
   - Verify API URL configuration
   - Test network requests

## 📊 Monitoring & Analytics

1. **Vercel Analytics**:
   - Enable in project settings
   - Monitor performance metrics
   - Track user interactions

2. **Error Tracking**:
   - Consider Sentry integration
   - Monitor function errors
   - Set up alerts

## 🔄 Continuous Deployment

1. **Automatic Deployments**:
   - Vercel automatically deploys on Git push
   - Configure branch protection rules
   - Use preview deployments for testing

2. **Environment Management**:
   - Use different environments for staging/production
   - Configure environment-specific variables
   - Test thoroughly before production deployment

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [React on Vercel](https://vercel.com/docs/frameworks/react)
- [PostgreSQL on Vercel](https://vercel.com/docs/storage/vercel-postgres)

## 🚀 Quick Reference

### Environment Variables Checklist
- [ ] `DATABASE_URL` - Database connection string
- [ ] `SECRET_KEY` - Strong secret for JWT tokens
- [ ] `ALGORITHM` - JWT algorithm (HS256)
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- [ ] `ALLOWED_ORIGINS` - Frontend domain for CORS
- [ ] `REACT_APP_API_URL` - Backend API URL (frontend only)

### Common Commands
```bash
# Check deployment status
vercel ls

# View deployment logs
vercel logs [deployment-url]

# Redeploy with environment variables
vercel --prod
```

### Configuration Files
- `vercel.json` - Root configuration (monorepo)
- `backend/vercel.json` - Backend-specific config
- `frontend/vercel.json` - Frontend-specific config
- `backend/requirements-vercel.txt` - Python dependencies

---

**Note**: This deployment guide assumes you have already resolved the NOT_FOUND error by installing the `pydantic[email]` dependency as documented in `BUGFIX_NOT_FOUND_ERROR.md`.
