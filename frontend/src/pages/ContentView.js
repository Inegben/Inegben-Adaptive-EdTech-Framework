import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import ReactPlayer from 'react-player';

const ContentView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [content, setContent] = useState(null);
  const [adaptiveData, setAdaptiveData] = useState(null);
  const [currentFormat, setCurrentFormat] = useState('video');
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    fetchContent();
    fetchProgress();
  }, [id]);

  useEffect(() => {
    if (content) {
      fetchAdaptiveContent();
    }
  }, [content]);

  const fetchContent = async () => {
    try {
      const response = await axios.get(`/api/v1/content/${id}`);
      setContent(response.data);
    } catch (error) {
      console.error('Failed to fetch content:', error);
      setError('Failed to load content');
      setLoading(false);
    }
  };

  const fetchAdaptiveContent = async () => {
    try {
      const response = await axios.get(`/api/v1/content/${id}/adaptive`);
      setAdaptiveData(response.data);
      setCurrentFormat(response.data.recommended_format);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch adaptive content:', error);
      setError('Failed to load adaptive content');
      setLoading(false);
    }
  };

  const fetchProgress = async () => {
    try {
      const response = await axios.get(`/api/v1/content/${id}/progress`);
      setProgress(response.data);
    } catch (error) {
      console.error('Failed to fetch progress:', error);
    }
  };

  const updateProgress = async (progressData) => {
    try {
      await axios.put(`/api/v1/content/${id}/progress`, progressData);
      setProgress(prev => ({ ...prev, ...progressData }));
    } catch (error) {
      console.error('Failed to update progress:', error);
    }
  };

  const recordInteraction = async (interactionType, metadata = {}) => {
    try {
      await axios.post(`/api/v1/content/${id}/interaction`, {
        interaction_type: interactionType,
        format_used: currentFormat,
        duration_seconds: 0,
        metadata
      });
    } catch (error) {
      console.error('Failed to record interaction:', error);
    }
  };

  const handleFormatChange = (format) => {
    setCurrentFormat(format);
    recordInteraction('format_switch', { from_format: currentFormat, to_format: format });
  };

  const handlePlay = () => {
    setIsPlaying(true);
    recordInteraction('play');
  };

  const handlePause = () => {
    setIsPlaying(false);
    recordInteraction('pause');
  };

  const handleProgress = (progressData) => {
    const percentage = progressData.played * 100;
    updateProgress({
      completion_percentage: percentage,
      last_position: progressData.playedSeconds
    });
  };

  const handleEnded = () => {
    setIsPlaying(false);
    updateProgress({
      completion_percentage: 100,
      is_completed: true
    });
    recordInteraction('completed');
  };

  const getFormatIcon = (format) => {
    switch (format) {
      case 'video': return '🎥';
      case 'audio': return '🎵';
      case 'text': return '📖';
      case 'interactive': return '🎮';
      default: return '📄';
    }
  };

  const getFormatLabel = (format) => {
    switch (format) {
      case 'video': return 'Video';
      case 'audio': return 'Audio';
      case 'text': return 'Text';
      case 'interactive': return 'Interactive';
      default: return 'Unknown';
    }
  };

  const renderContent = () => {
    if (!content) return null;

    switch (currentFormat) {
      case 'video':
        return content.video_url ? (
          <div className="video-player">
            <ReactPlayer
              url={content.video_url}
              width="100%"
              height="400px"
              controls
              playing={isPlaying}
              onPlay={handlePlay}
              onPause={handlePause}
              onProgress={handleProgress}
              onEnded={handleEnded}
            />
          </div>
        ) : (
          <div className="format-unavailable">
            <p>Video format not available for this content.</p>
          </div>
        );

      case 'audio':
        return content.audio_url ? (
          <div className="audio-player">
            <ReactPlayer
              url={content.audio_url}
              width="100%"
              height="80px"
              controls
              playing={isPlaying}
              onPlay={handlePlay}
              onPause={handlePause}
              onProgress={handleProgress}
              onEnded={handleEnded}
            />
            {content.text_content && (
              <div className="audio-transcript">
                <h4>Transcript</h4>
                <div className="transcript-content">
                  {content.text_content}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="format-unavailable">
            <p>Audio format not available for this content.</p>
          </div>
        );

      case 'text':
        return content.text_content ? (
          <div className="text-content">
            <div className="text-content-body">
              {content.text_content}
            </div>
          </div>
        ) : (
          <div className="format-unavailable">
            <p>Text format not available for this content.</p>
          </div>
        );

      case 'interactive':
        return content.interactive_url ? (
          <div className="interactive-content">
            <iframe
              src={content.interactive_url}
              width="100%"
              height="500px"
              frameBorder="0"
              title="Interactive Content"
            />
          </div>
        ) : (
          <div className="format-unavailable">
            <p>Interactive format not available for this content.</p>
          </div>
        );

      default:
        return (
          <div className="format-unavailable">
            <p>Selected format not available.</p>
          </div>
        );
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading content...</p>
      </div>
    );
  }

  if (error || !content) {
    return (
      <div className="error-message">
        <p>{error || 'Content not found'}</p>
        <button onClick={() => navigate('/dashboard')} className="btn btn-primary">
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="content-container">
      <div className="content-header">
        <div>
          <h1 className="content-title">{content.title}</h1>
          <div className="content-meta">
            <span>{content.subject}</span>
            <span>{content.difficulty_level}</span>
            <span>{content.duration_minutes} min</span>
          </div>
        </div>
        
        {adaptiveData && (
          <div className="format-toggle">
            {['video', 'audio', 'text', 'interactive'].map((format) => {
              const isAvailable = content[`${format}_url`] || (format === 'text' && content.text_content);
              if (!isAvailable) return null;
              
              return (
                <button
                  key={format}
                  className={`format-button ${currentFormat === format ? 'active' : ''}`}
                  onClick={() => handleFormatChange(format)}
                  title={`Switch to ${getFormatLabel(format)} format`}
                >
                  <span className="format-icon">{getFormatIcon(format)}</span>
                  <span className="format-label">{getFormatLabel(format)}</span>
                </button>
              );
            })}
          </div>
        )}
      </div>

      {adaptiveData && (
        <div className="personalization-info">
          <p>
            <strong>Personalized for you:</strong> {adaptiveData.personalization_reason}
          </p>
        </div>
      )}

      <div className="content-player">
        {renderContent()}
      </div>

      {progress && (
        <div className="progress-info">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress.completion_percentage}%` }}
            ></div>
          </div>
          <div className="progress-stats">
            <span>{Math.round(progress.completion_percentage)}% Complete</span>
            <span>{progress.time_spent_minutes} min spent</span>
            {progress.is_completed && <span className="completed-badge">✓ Completed</span>}
          </div>
        </div>
      )}

      <div className="content-description">
        <h3>About this content</h3>
        <p>{content.description || 'No description available.'}</p>
        
        {content.learning_objectives && content.learning_objectives.length > 0 && (
          <div className="learning-objectives">
            <h4>Learning Objectives</h4>
            <ul>
              {content.learning_objectives.map((objective, index) => (
                <li key={index}>{objective}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ContentView;
