import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const Assessment = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      const response = await axios.get('/api/v1/assessment/questions');
      setQuestions(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch questions:', error);
      setError('Failed to load assessment questions');
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, answer) => {
    setAnswers({
      ...answers,
      [questionId]: answer
    });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length !== questions.length) {
      setError('Please answer all questions before submitting');
      return;
    }

    setSubmitting(true);
    setError('');

    try {
      const submission = {
        answers: Object.entries(answers).map(([questionId, answer]) => ({
          question_id: parseInt(questionId),
          answer: answer
        }))
      };

      const response = await axios.post('/api/v1/assessment/submit', submission);
      
      // Update user context with new learning style
      await updateUser({ learning_style: response.data.learning_style });
      
      // Navigate to dashboard with success message
      navigate('/dashboard', { 
        state: { 
          message: `Great! You're a ${response.data.learning_style} learner. Your content will now be personalized for you.`,
          learningStyle: response.data.learning_style
        }
      });
    } catch (error) {
      console.error('Assessment submission failed:', error);
      setError('Failed to submit assessment. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const progress = ((currentQuestion + 1) / questions.length) * 100;

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading assessment...</p>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="error-message">
        <p>No assessment questions available. Please try again later.</p>
      </div>
    );
  }

  const question = questions[currentQuestion];
  const currentAnswer = answers[question.id];

  return (
    <div className="assessment-container">
      <div className="assessment-header">
        <h1>Learning Style Assessment</h1>
        <p>Answer these questions to discover your optimal learning style</p>
      </div>

      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${progress}%` }}
        ></div>
      </div>

      <div className="question-card">
        <div className="question-number">
          Question {currentQuestion + 1} of {questions.length}
        </div>
        
        <h2 className="question-text">{question.question_text}</h2>

        <div className="radio-group">
          <label 
            className={`radio-option ${currentAnswer === 'visual' ? 'selected' : ''}`}
            onClick={() => handleAnswerSelect(question.id, 'visual')}
          >
            <input
              type="radio"
              name={`question_${question.id}`}
              value="visual"
              checked={currentAnswer === 'visual'}
              onChange={() => handleAnswerSelect(question.id, 'visual')}
            />
            <div>
              <strong>Visual:</strong> {question.visual_answer}
            </div>
          </label>

          <label 
            className={`radio-option ${currentAnswer === 'auditory' ? 'selected' : ''}`}
            onClick={() => handleAnswerSelect(question.id, 'auditory')}
          >
            <input
              type="radio"
              name={`question_${question.id}`}
              value="auditory"
              checked={currentAnswer === 'auditory'}
              onChange={() => handleAnswerSelect(question.id, 'auditory')}
            />
            <div>
              <strong>Auditory:</strong> {question.auditory_answer}
            </div>
          </label>

          <label 
            className={`radio-option ${currentAnswer === 'kinesthetic' ? 'selected' : ''}`}
            onClick={() => handleAnswerSelect(question.id, 'kinesthetic')}
          >
            <input
              type="radio"
              name={`question_${question.id}`}
              value="kinesthetic"
              checked={currentAnswer === 'kinesthetic'}
              onChange={() => handleAnswerSelect(question.id, 'kinesthetic')}
            />
            <div>
              <strong>Kinesthetic:</strong> {question.kinesthetic_answer}
            </div>
          </label>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <div className="assessment-navigation">
          <button
            type="button"
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            className="btn btn-secondary"
          >
            Previous
          </button>

          <div className="question-indicators">
            {questions.map((_, index) => (
              <div
                key={index}
                className={`indicator ${index === currentQuestion ? 'active' : ''} ${
                  answers[questions[index].id] ? 'answered' : ''
                }`}
                onClick={() => setCurrentQuestion(index)}
              />
            ))}
          </div>

          {currentQuestion === questions.length - 1 ? (
            <button
              type="button"
              onClick={handleSubmit}
              disabled={submitting || Object.keys(answers).length !== questions.length}
              className="btn btn-primary"
            >
              {submitting ? 'Submitting...' : 'Complete Assessment'}
            </button>
          ) : (
            <button
              type="button"
              onClick={handleNext}
              disabled={!currentAnswer}
              className="btn btn-primary"
            >
              Next
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Assessment;
