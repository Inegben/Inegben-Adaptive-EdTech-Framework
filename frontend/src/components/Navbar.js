import * as React from 'react';
const { useState } = React;
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMenuOpen(false);
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="navbar-brand">
            <span className="brand-icon">🎓</span>
            IAEF
          </Link>

          <div className={`navbar-menu ${isMenuOpen ? 'active' : ''}`}>
            <div className="navbar-links">
              <Link to="/" className="navbar-link">Home</Link>
              {user && (
                <>
                  <Link to="/dashboard" className="navbar-link">Dashboard</Link>
                  {!user.assessment_completed && (
                    <Link to="/assessment" className="navbar-link">Assessment</Link>
                  )}
                </>
              )}
            </div>

            <div className="navbar-auth">
              {user ? (
                <div className="user-menu">
                  <div className="user-info">
                    <span className="user-name">{user.username}</span>
                    {user.learning_style && (
                      <span className="learning-style">
                        {user.learning_style.charAt(0).toUpperCase() + user.learning_style.slice(1)} Learner
                      </span>
                    )}
                  </div>
                  <button onClick={handleLogout} className="btn btn-outline btn-sm">
                    Logout
                  </button>
                </div>
              ) : (
                <div className="auth-buttons">
                  <Link to="/login" className="btn btn-outline btn-sm">
                    Login
                  </Link>
                  <Link to="/register" className="btn btn-primary btn-sm">
                    Sign Up
                  </Link>
                </div>
              )}
            </div>
          </div>

          <button 
            className="navbar-toggle"
            onClick={toggleMenu}
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
