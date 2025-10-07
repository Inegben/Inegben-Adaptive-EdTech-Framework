# Inegben Adaptive EdTech Framework (IAEF)

A comprehensive educational technology framework designed to provide adaptive learning experiences for students across various educational levels.

## 🎯 Overview

The IAEF addresses the critical need for personalized learning experiences in educational technology. Many existing EdTech platforms fail to account for individual learning styles, leading to decreased user engagement and content retention. IAEF solves this by providing a highly personalized learning experience that adapts content delivery based on the user's identified preferences.

## ✨ Key Features

### 🧠 Learning Style Assessment
- 10-question assessment to identify learning style (Visual, Auditory, Kinesthetic)
- Automatic content personalization based on assessment results
- Manual learning style adjustment in user profile

### 🔄 Adaptive Content Delivery
- Dynamic content format selection based on learning style
- Performance-based format switching recommendations
- Real-time adaptation based on user interaction patterns

### 🎮 Instant Format Toggle
- Seamless switching between video, audio, text, and interactive formats
- No page reload required - maintains learning progress
- Visual indicators for available formats

### 📊 Progress Tracking & Analytics
- Real-time progress monitoring
- Engagement metrics and learning analytics
- Personalized content recommendations

### 🎓 Multi-Format Content Support
- Video tutorials and demonstrations
- Audio lectures with transcripts
- Interactive simulations and exercises
- Text-based learning materials

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **User Service**: Authentication, profiles, learning styles
- **Adaptive Engine**: Core logic for content personalization
- **Analytics Service**: User interaction tracking and insights
- **Content Management**: Multi-format content delivery
- **Database**: PostgreSQL with SQLAlchemy ORM

### Frontend (React)
- **Responsive Web Application**: Works on desktop and mobile
- **Authentication System**: Secure user registration and login
- **Assessment Interface**: Interactive learning style assessment
- **Adaptive Content Viewer**: Multi-format content player
- **Dashboard**: Progress tracking and recommendations

### Database Schema
- **Users**: Authentication, learning preferences, assessment results
- **Content**: Multi-format educational materials
- **Progress Records**: Learning progress and completion tracking
- **Content Interactions**: Detailed user engagement analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Inegben/Inegben-Adaptive-EdTech-Framework.git
   cd Inegben-Adaptive-EdTech-Framework
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure database**
   - Create PostgreSQL database: `createdb iaef_db`
   - Update `backend/.env` with your database credentials

4. **Start the servers**
   
   Backend:
   ```bash
   cd backend
   source venv/bin/activate
   python run.py
   ```
   
   Frontend:
   ```bash
   cd frontend
   npm start
   ```

5. **Access the application**
   - Open http://localhost:3000 in your browser
   - Register a new account or use sample users

### Sample Users
- **alex@example.com** / alex_student (Visual Learner)
- **sarah@example.com** / sarah_professional (Auditory Learner)  
- **mike@example.com** / mike_learner (Kinesthetic Learner)
- Password for all: `password123`

## 📋 User Stories & Features

### Epic 1: User Onboarding & Personalization
- ✅ Learning Style Assessment (10 questions)
- ✅ Profile Style Management
- ✅ Automatic content personalization

### Epic 2: Adaptive Content Delivery Engine
- ✅ Visual Content Prioritization
- ✅ Auditory Content Prioritization
- ✅ Performance-Based Format Switch

### Epic 3: Learning Control & Feedback
- ✅ Instant Format Toggle
- ✅ Progress Tracking Dashboard
- ✅ Personalized Recommendations

## 🎯 Learning Styles

### Visual Learners 👁️
- Prefer videos, infographics, mind maps
- Learn through visual representations
- Benefit from diagrams and charts

### Auditory Learners 👂
- Thrive on audiobooks, podcasts, lectures
- Learn through listening and discussion
- Prefer verbal explanations

### Kinesthetic Learners ✋
- Learn best through hands-on activities
- Prefer interactive simulations
- Benefit from physical interaction

## 📊 Success Metrics

- **Engagement Rate**: Daily Active Users (DAU) and session duration
- **Retention Rate**: Percentage of users returning weekly/monthly
- **Completion Rate**: Percentage of users completing courses/modules
- **User Satisfaction**: Measured via surveys and in-app feedback
- **Learning Outcomes**: Measurable improvement in quiz/test performance

## 🛠️ Technical Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy
- **Authentication**: JWT tokens with bcrypt
- **API Documentation**: Automatic OpenAPI/Swagger
- **Migrations**: Alembic

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Media Player**: React Player
- **Styling**: CSS3 with modern features

### Development Tools
- **Package Management**: pip (Python), npm (Node.js)
- **Code Quality**: ESLint, Prettier
- **Version Control**: Git
- **Database Migrations**: Alembic

## 📁 Project Structure

```
IAEF/
├── backend/
│   ├── app/
│   │   ├── core/          # Configuration and settings
│   │   ├── models/        # Database models
│   │   ├── routers/       # API endpoints
│   │   ├── schemas/       # Pydantic schemas
│   │   └── main.py        # FastAPI application
│   ├── alembic/           # Database migrations
│   ├── scripts/           # Utility scripts
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── contexts/      # React contexts
│   │   ├── pages/         # Application pages
│   │   └── App.js         # Main application
│   └── package.json       # Node.js dependencies
├── docs/                  # Documentation
└── README.md             # This file
```

## 🔧 API Endpoints

### Authentication
- `POST /api/v1/users/register` - User registration
- `POST /api/v1/users/login` - User login
- `GET /api/v1/users/me` - Get current user

### Assessment
- `GET /api/v1/assessment/questions` - Get assessment questions
- `POST /api/v1/assessment/submit` - Submit assessment answers
- `GET /api/v1/assessment/result` - Get assessment result

### Content
- `GET /api/v1/content/` - List all content
- `GET /api/v1/content/{id}` - Get specific content
- `GET /api/v1/content/{id}/adaptive` - Get adaptive content
- `POST /api/v1/content/{id}/interaction` - Record interaction
- `GET /api/v1/content/recommendations/personalized` - Get recommendations

### Analytics
- `GET /api/v1/analytics/dashboard/overview` - Dashboard overview
- `GET /api/v1/analytics/user/{id}` - User analytics
- `GET /api/v1/analytics/content/{id}` - Content analytics

## 🚀 Deployment

The IAEF application supports multiple deployment platforms. Choose the one that best fits your needs:

### 🌟 Platform Comparison

| Feature | Vercel | Netlify |
|---------|--------|---------|
| **Frontend Hosting** | ✅ Static Site | ✅ Static Site |
| **Backend Functions** | ✅ Python/FastAPI | ✅ Python/FastAPI |
| **Database Integration** | ✅ Vercel Postgres | ✅ External DBs |
| **Build Process** | ✅ Auto-detected | ✅ Configurable |
| **Custom Domains** | ✅ Free | ✅ Free |
| **Preview Deployments** | ✅ Automatic | ✅ Automatic |
| **Cold Start Performance** | ✅ Fast | ✅ Fast |

### 🚀 Vercel Deployment (Recommended)

**Best for**: Integrated database solutions and automatic deployments

📖 **Complete Guide**: [VERCEL_DEPLOYMENT_COMPLETE.md](VERCEL_DEPLOYMENT_COMPLETE.md)

**Quick Setup:**
1. **Backend**: Deploy as serverless function with `backend/vercel.json`
2. **Frontend**: Deploy as static site with `frontend/vercel.json`
3. **Database**: Use Vercel Postgres or external PostgreSQL
4. **Environment Variables**: Configure in Vercel dashboard

**Advantages:**
- ✅ Integrated Vercel Postgres database
- ✅ Automatic framework detection
- ✅ Excellent Python serverless support
- ✅ Built-in analytics and monitoring

### 🌐 Netlify Deployment (Alternative)

**Best for**: Custom build processes and external database services

📖 **Complete Guide**: [NETLIFY_DEPLOYMENT.md](NETLIFY_DEPLOYMENT.md)

**Quick Setup:**
1. **Frontend**: Deploy as static site with `netlify.toml`
2. **Backend**: Deploy as serverless functions with `netlify/functions/`
3. **Database**: Use Supabase, PlanetScale, or Railway PostgreSQL
4. **Environment Variables**: Configure in Netlify dashboard

**Advantages:**
- ✅ Flexible build configuration
- ✅ Excellent external database support
- ✅ Advanced form handling
- ✅ Built-in A/B testing
- ✅ Edge functions support

### 🎯 One-Click Deploy

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Inegben/Inegben-Adaptive-EdTech-Framework)

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/Inegben/Inegben-Adaptive-EdTech-Framework)

### 📁 Deployment Configuration Files

The repository includes all necessary configuration files for both platforms:

#### Vercel Configuration
- `vercel.json` - Root monorepo configuration
- `backend/vercel.json` - Backend serverless function config
- `frontend/vercel.json` - Frontend static site config
- `backend/requirements.txt` - Python dependencies

#### Netlify Configuration
- `netlify.toml` - Main Netlify configuration
- `netlify/functions/api.py` - FastAPI adapter for Netlify Functions
- `netlify/functions/requirements.txt` - Serverless dependencies
- `backend/netlify_config.py` - Netlify-specific settings
- `backend/app/netlify_main.py` - Optimized FastAPI app

#### Frontend Configuration
- `frontend/package.json` - Node.js dependencies and scripts
- `frontend/src/config/api.js` - Centralized API configuration
- `frontend/.env.example` - Environment variable template

### Traditional Deployment

#### Backend Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Run database migrations: `alembic upgrade head`
4. Deploy with gunicorn or similar WSGI server

#### Frontend Deployment
1. Build the application: `npm run build`
2. Serve static files with nginx or similar
3. Configure API endpoint URLs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Educational psychology research on learning styles
- Modern web development best practices
- Open source community contributions

## 🐛 Known Issues & Bug Fixes

### Recent Bug Fixes
- **NOT_FOUND Error (Oct 2025)**: Resolved missing `email-validator` dependency that prevented FastAPI app startup
  - See [BUGFIX_NOT_FOUND_ERROR.md](BUGFIX_NOT_FOUND_ERROR.md) for detailed documentation
  - **Solution**: Install `pydantic[email]` extra for EmailStr validation support

### Troubleshooting
If you encounter 404 errors on all endpoints:
1. Check if the backend server is running: `python run.py`
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Ensure email validation extras are installed: `pip install pydantic[email]`

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the [bug fix documentation](BUGFIX_NOT_FOUND_ERROR.md) for common issues
- Contact: [stanleyinegben@gmail.com]

---

**Built with ❤️ for better education through technology by Inegben Stanley**
