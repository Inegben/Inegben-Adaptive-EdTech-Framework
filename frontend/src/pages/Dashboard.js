import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const { user } = useAuth();
  const location = useLocation();

  useEffect(() => {
    fetchDashboardData();
    fetchRecommendations();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get('/api/v1/analytics/dashboard/overview');
      setDashboardData(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const fetchRecommendations = async () => {
    try {
      const response = await axios.get('/api/v1/content/recommendations/personalized?limit=6');
      setRecommendations(response.data);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
    }
  };

  const getLearningStyleIcon = (style) => {
    switch (style) {
      case 'visual': return '👁️';
      case 'auditory': return '👂';
      case 'kinesthetic': return '✋';
      default: return '🎓';
    }
  };


  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading your dashboard...</p>
      </div>
    );
  }

  const successMessage = location.state?.message;

  return (
    <div className="dashboard-container">
      {successMessage && (
        <div className="success-message">
          {successMessage}
        </div>
      )}

      <div className="dashboard-header">
        <h1>Welcome back, {user?.username}!</h1>
        <p>Continue your personalized learning journey</p>
      </div>

      {user?.learning_style && (
        <div className="learning-style-badge">
          <span className="style-icon">{getLearningStyleIcon(user.learning_style)}</span>
          <span className="style-text">
            {user.learning_style.charAt(0).toUpperCase() + user.learning_style.slice(1)} Learner
          </span>
        </div>
      )}

      {dashboardData && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{dashboardData.total_time_minutes || 0}</div>
            <div className="stat-label">Minutes Learned</div>
          </div>
          
          <div className="stat-card">
            <div className="stat-value">{dashboardData.content_completed || 0}</div>
            <div className="stat-label">Content Completed</div>
          </div>
          
          <div className="stat-card">
            <div className="stat-value">{dashboardData.content_in_progress || 0}</div>
            <div className="stat-label">In Progress</div>
          </div>
          
          <div className="stat-card">
            <div className="stat-value">
              {dashboardData.assessment_completed ? '✓' : '⚠️'}
            </div>
            <div className="stat-label">
              {dashboardData.assessment_completed ? 'Assessment Complete' : 'Assessment Pending'}
            </div>
          </div>
        </div>
      )}

      {!user?.assessment_completed && (
        <div className="assessment-prompt">
          <div className="prompt-content">
            <h3>🎯 Complete Your Learning Assessment</h3>
            <p>
              Take our quick 10-question assessment to discover your learning style 
              and get personalized content recommendations.
            </p>
            <Link to="/assessment" className="btn btn-primary">
              Take Assessment
            </Link>
          </div>
        </div>
      )}

      <div className="dashboard-sections">
        <div className="section">
          <div className="section-header">
            <h2>Recommended for You</h2>
            <p>Content tailored to your learning style</p>
          </div>
          
          {recommendations.length > 0 ? (
            <div className="content-grid">
              {recommendations.map((content) => (
                <div key={content.id} className="content-card">
                  <div className="content-card-header">
                    <h3 className="content-card-title">{content.title}</h3>
                    <div className="content-card-meta">
                      <span>{content.subject}</span>
                      <span>{content.difficulty_level}</span>
                      <span>{content.duration_minutes} min</span>
                    </div>
                  </div>
                  
                  <div className="content-card-body">
                    <p className="content-card-description">
                      {content.description || 'No description available'}
                    </p>
                  </div>
                  
                  <div className="content-card-footer">
                    <Link 
                      to={`/content/${content.id}`} 
                      className="btn btn-primary"
                    >
                      Start Learning
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No recommendations available. Complete your assessment to get personalized content!</p>
            </div>
          )}
        </div>

        {dashboardData?.format_usage && Object.keys(dashboardData.format_usage).length > 0 && (
          <div className="section">
            <div className="section-header">
              <h2>Your Learning Preferences</h2>
              <p>Based on your interaction history</p>
            </div>
            
            <div className="preferences-grid">
              {Object.entries(dashboardData.format_usage).map(([format, count]) => (
                <div key={format} className="preference-card">
                  <div className="preference-icon">
                    {format === 'video' ? '🎥' : 
                     format === 'audio' ? '🎵' : 
                     format === 'text' ? '📖' : '🎮'}
                  </div>
                  <div className="preference-info">
                    <h4>{format.charAt(0).toUpperCase() + format.slice(1)}</h4>
                    <p>{count} interactions</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
