import React, { useState } from 'react';
import axios from 'axios';

const ApiTest = () => {
  const [testResults, setTestResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const addResult = (test, status, message, data = null) => {
    setTestResults(prev => [...prev, {
      test,
      status,
      message,
      data,
      timestamp: new Date().toLocaleTimeString()
    }]);
  };

  const testApiConnection = async () => {
    setLoading(true);
    setTestResults([]);
    
    try {
      // Test 1: Basic API endpoint
      addResult('API Connection', 'Testing', 'Testing basic API connection...');
      
      const response = await axios.get('/api/v1/analytics/dashboard/overview');
      addResult('API Connection', 'Success', 'API is responding', response.data);
      
    } catch (error) {
      addResult('API Connection', 'Error', `API connection failed: ${error.message}`, {
        status: error.response?.status,
        data: error.response?.data
      });
    }

    // Test 2: Login endpoint
    try {
      addResult('Login Test', 'Testing', 'Testing login with sample user...');
      
      const response = await axios.post('/api/v1/users/login', null, {
        params: { 
          email: 'alex@example.com', 
          password: 'password123' 
        }
      });
      
      addResult('Login Test', 'Success', 'Login successful', response.data);
      
    } catch (error) {
      addResult('Login Test', 'Error', `Login failed: ${error.message}`, {
        status: error.response?.status,
        data: error.response?.data
      });
    }

    // Test 3: Assessment endpoint
    try {
      addResult('Assessment Test', 'Testing', 'Testing assessment questions...');
      
      const response = await axios.get('/api/v1/assessment/questions');
      addResult('Assessment Test', 'Success', 'Assessment questions loaded', response.data);
      
    } catch (error) {
      addResult('Assessment Test', 'Error', `Assessment failed: ${error.message}`, {
        status: error.response?.status,
        data: error.response?.data
      });
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2>API Test Dashboard</h2>
      <p>This will test all API endpoints to see what's working and what's not.</p>
      
      <button 
        onClick={testApiConnection} 
        disabled={loading}
        style={{
          padding: '10px 20px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: loading ? 'not-allowed' : 'pointer',
          marginBottom: '20px'
        }}
      >
        {loading ? 'Testing...' : 'Run API Tests'}
      </button>

      {testResults.length > 0 && (
        <div>
          <h3>Test Results:</h3>
          {testResults.map((result, index) => (
            <div 
              key={index}
              style={{
                padding: '10px',
                margin: '10px 0',
                border: '1px solid #ddd',
                borderRadius: '5px',
                backgroundColor: result.status === 'Success' ? '#d4edda' : 
                               result.status === 'Error' ? '#f8d7da' : '#fff3cd'
              }}
            >
              <div style={{ fontWeight: 'bold' }}>
                {result.test} - {result.status} ({result.timestamp})
              </div>
              <div style={{ margin: '5px 0' }}>{result.message}</div>
              {result.data && (
                <details style={{ marginTop: '10px' }}>
                  <summary>Response Data</summary>
                  <pre style={{ 
                    backgroundColor: '#f8f9fa', 
                    padding: '10px', 
                    borderRadius: '3px',
                    overflow: 'auto',
                    fontSize: '12px'
                  }}>
                    {JSON.stringify(result.data, null, 2)}
                  </pre>
                </details>
              )}
            </div>
          ))}
        </div>
      )}

      <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
        <h4>Sample Users for Testing:</h4>
        <ul>
          <li><strong>alex@example.com</strong> / password123 (Visual Learner)</li>
          <li><strong>sarah@example.com</strong> / password123 (Auditory Learner)</li>
          <li><strong>mike@example.com</strong> / password123 (Kinesthetic Learner)</li>
        </ul>
      </div>
    </div>
  );
};

export default ApiTest;
