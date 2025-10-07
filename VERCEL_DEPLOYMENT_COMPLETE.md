# Complete Vercel Deployment Guide - IAEF

## 🚨 CRITICAL: Deploy as Separate Projects

**DO NOT** try to deploy as a monorepo. Deploy frontend and backend as **separate Vercel projects**.

## 🎯 Step-by-Step Deployment

### 1. Backend Deployment

#### A. Create Backend Project
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. **Configure Project**:
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: Leave empty (auto-detected)
   - **Output Directory**: Leave empty (serverless function)

#### B. Set Environment Variables
Go to Project Settings → Environment Variables and add:

| Variable | Value | Environments |
|----------|-------|--------------|
| `DATABASE_URL` | `postgresql://user:pass@host:port/db` | Production, Preview, Development |
| `SECRET_KEY` | `your-256-bit-secret-key-here` | Production, Preview, Development |
| `ALGORITHM` | `HS256` | Production, Preview, Development |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Production, Preview, Development |
| `ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` | Production, Preview, Development |

#### C. Deploy
- Click "Deploy"
- Note the backend URL (e.g., `https://iaef-backend.vercel.app`)

### 2. Frontend Deployment

#### A. Create Frontend Project
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import the same GitHub repository
4. **Configure Project**:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

#### B. Set Environment Variables
Go to Project Settings → Environment Variables and add:

| Variable | Value | Environments |
|----------|-------|--------------|
| `REACT_APP_API_URL` | `https://your-backend.vercel.app` | Production, Preview, Development |

#### C. Deploy
- Click "Deploy"
- Note the frontend URL (e.g., `https://iaef-frontend.vercel.app`)

### 3. Update CORS Configuration

After both deployments:
1. Go to your backend project settings
2. Update `ALLOWED_ORIGINS` environment variable:
   ```
   https://your-frontend.vercel.app,https://your-custom-domain.com
   ```
3. Redeploy the backend

## 🗄️ Database Setup

### Option 1: Vercel Postgres (Recommended)
1. Go to your backend project
2. Click "Storage" tab
3. Create new Postgres database
4. Copy connection string to `DATABASE_URL`

### Option 2: Supabase (Free)
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Go to Settings → Database
4. Copy connection string to `DATABASE_URL`

### Option 3: PlanetScale (MySQL)
1. Go to [planetscale.com](https://planetscale.com)
2. Create new database
3. Copy connection string to `DATABASE_URL`

## 🔧 Configuration Files

### Backend (`backend/vercel.json`)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}
```

### Frontend (`frontend/vercel.json`)
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
  ]
}
```

## 🐛 Common Issues & Solutions

### 1. Build Failures
- **Error**: "Could not find index.html"
- **Solution**: Ensure Root Directory is set to `frontend` for frontend project

### 2. Environment Variables
- **Error**: "Secret does not exist"
- **Solution**: Use regular environment variables, NOT secrets

### 3. CORS Errors
- **Error**: CORS policy blocks requests
- **Solution**: Update `ALLOWED_ORIGINS` with your frontend URL

### 4. Database Connection
- **Error**: Database connection failed
- **Solution**: Check `DATABASE_URL` format and credentials

### 5. Function Timeout
- **Error**: Function execution timeout
- **Solution**: Optimize database queries, add caching

## 🚀 Testing Your Deployment

### Backend Health Check
```bash
curl https://your-backend.vercel.app/health
```

### Frontend Access
Visit: `https://your-frontend.vercel.app`

### API Test
```bash
curl https://your-backend.vercel.app/api/v1/users/me
```

## 📊 Monitoring

1. **Vercel Analytics**: Enable in project settings
2. **Function Logs**: Check in Vercel dashboard
3. **Error Tracking**: Consider Sentry integration

## 🔄 Continuous Deployment

- Automatic deploys on Git push
- Preview deployments for pull requests
- Environment-specific configurations

## 🆘 Troubleshooting

### Check Build Logs
1. Go to project dashboard
2. Click on latest deployment
3. View build logs for errors

### Verify Environment Variables
1. Go to project settings
2. Check Environment Variables section
3. Ensure all required variables are set

### Test Locally First
```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm start
```

---

**Remember**: Deploy as separate projects for best results! 🎯
