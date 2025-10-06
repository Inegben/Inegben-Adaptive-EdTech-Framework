import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Home = () => {
  const { user } = useAuth();

  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <h1>Find Your Perfect Learning Style</h1>
          <p>
            Discover how you learn best with our adaptive educational framework. 
            Get personalized content that matches your unique learning preferences.
          </p>
          <div className="hero-buttons">
            {user ? (
              <>
                <Link to="/dashboard" className="btn btn-primary">
                  Go to Dashboard
                </Link>
                {!user.assessment_completed && (
                  <Link to="/assessment" className="btn btn-outline">
                    Take Assessment
                  </Link>
                )}
              </>
            ) : (
              <>
                <Link to="/register" className="btn btn-primary">
                  Get Started
                </Link>
                <Link to="/login" className="btn btn-outline">
                  Sign In
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="container">
          <h2>Why Choose IAEF?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Personalized Learning</h3>
              <p>
                Our assessment identifies your learning style and adapts content 
                delivery to match your preferences for maximum engagement.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🔄</div>
              <h3>Adaptive Content</h3>
              <p>
                Switch between visual, auditory, and interactive formats instantly. 
                The system learns from your interactions to improve recommendations.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Progress Tracking</h3>
              <p>
                Monitor your learning journey with detailed analytics and insights 
                that help you understand your progress and areas for improvement.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🎓</div>
              <h3>Multi-Format Support</h3>
              <p>
                Access content in videos, audio, text, and interactive formats. 
                Perfect for different learning contexts and preferences.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Instant Format Toggle</h3>
              <p>
                Switch between content formats without losing your place. 
                Seamlessly transition between learning modes as needed.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🧠</div>
              <h3>Smart Recommendations</h3>
              <p>
                Get content suggestions based on your learning style, progress, 
                and engagement patterns for a truly personalized experience.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Learning Styles Section */}
      <section className="learning-styles">
        <div className="container">
          <h2>Discover Your Learning Style</h2>
          <div className="styles-grid">
            <div className="style-card visual">
              <div className="style-icon">👁️</div>
              <h3>Visual Learners</h3>
              <p>
                Learn best through images, diagrams, videos, and visual representations. 
                Prefer to see information rather than hear it.
              </p>
              <ul>
                <li>Video tutorials and demonstrations</li>
                <li>Infographics and charts</li>
                <li>Mind maps and diagrams</li>
                <li>Color-coded information</li>
              </ul>
            </div>
            
            <div className="style-card auditory">
              <div className="style-icon">👂</div>
              <h3>Auditory Learners</h3>
              <p>
                Learn best through listening, discussions, and verbal explanations. 
                Prefer to hear information and process it through sound.
              </p>
              <ul>
                <li>Audio lectures and podcasts</li>
                <li>Group discussions</li>
                <li>Verbal instructions</li>
                <li>Background music while studying</li>
              </ul>
            </div>
            
            <div className="style-card kinesthetic">
              <div className="style-icon">✋</div>
              <h3>Kinesthetic Learners</h3>
              <p>
                Learn best through hands-on activities, movement, and physical interaction. 
                Prefer to learn by doing and experiencing.
              </p>
              <ul>
                <li>Interactive simulations</li>
                <li>Hands-on experiments</li>
                <li>Physical activities</li>
                <li>Building and creating</li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
