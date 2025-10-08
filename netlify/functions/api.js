exports.handler = async (event, context) => {
  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  try {
    const method = event.httpMethod;
    const path = event.path;
    
    console.log(`Request: ${method} ${path}`);

    // Test endpoint
    if (path === '/api/v1/test' && method === 'GET') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          message: 'API is working!',
          path: path,
          method: method,
          timestamp: new Date().toISOString()
        })
      };
    }

    // Login endpoint
    if (path === '/api/v1/users/login' && method === 'POST') {
      const queryParams = event.queryStringParameters || {};
      const email = queryParams.email;
      const password = queryParams.password;
      
      console.log(`Login attempt: ${email}`);

      if (email === 'alex@example.com' && password === 'password123') {
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            access_token: 'demo_token_123',
            token_type: 'bearer',
            user: {
              id: 1,
              email: 'alex@example.com',
              username: 'alex_student',
              learning_style: 'visual',
              assessment_completed: true
            }
          })
        };
      } else {
        return {
          statusCode: 401,
          headers,
          body: JSON.stringify({ detail: 'Invalid credentials' })
        };
      }
    }

    // Register endpoint
    if (path === '/api/v1/users/register' && method === 'POST') {
      const body = JSON.parse(event.body || '{}');
      const email = body.email;
      const username = body.username;
      const password = body.password;
      
      console.log(`Registration attempt: ${email}`);

      if (email && username && password) {
        return {
          statusCode: 201,
          headers,
          body: JSON.stringify({
            access_token: 'demo_token_456',
            token_type: 'bearer',
            user: {
              id: 999,
              email: email,
              username: username,
              learning_style: null,
              assessment_completed: false
            }
          })
        };
      } else {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ detail: 'Email, username, and password are required' })
        };
      }
    }

    // Dashboard endpoint
    if (path === '/api/v1/analytics/dashboard/overview' && method === 'GET') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          total_time_minutes: 120,
          content_completed: 2,
          content_in_progress: 1,
          assessment_completed: true,
          format_usage: {
            video: 5,
            text: 3,
            audio: 1,
            interactive: 2
          }
        })
      };
    }

    // Assessment questions endpoint
    if (path === '/api/v1/assessment/questions' && method === 'GET') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify([
          {
            id: 1,
            question_text: "When learning something new, I prefer to:",
            visual_answer: "See diagrams, charts, and visual representations",
            auditory_answer: "Listen to explanations and discussions",
            kinesthetic_answer: "Try it out hands-on and practice"
          },
          {
            id: 2,
            question_text: "I remember information best when I:",
            visual_answer: "Write it down or see it written",
            auditory_answer: "Hear it spoken or discuss it",
            kinesthetic_answer: "Do something with it or experience it"
          }
        ])
      };
    }

    // Assessment submit endpoint
    if (path === '/api/v1/assessment/submit' && method === 'POST') {
      const body = JSON.parse(event.body || '{}');
      const answers = body.answers || [];
      
      if (answers.length === 0) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ detail: 'Answers are required' })
        };
      }

      // Count answers by learning style
      const styleCounts = { visual: 0, auditory: 0, kinesthetic: 0 };
      
      answers.forEach(answer => {
        const style = answer.answer;
        if (styleCounts.hasOwnProperty(style)) {
          styleCounts[style]++;
        }
      });

      // Determine learning style
      const learningStyle = Object.keys(styleCounts).reduce((a, b) => 
        styleCounts[a] > styleCounts[b] ? a : b
      );

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          learning_style: learningStyle,
          scores: styleCounts,
          message: `Based on your answers, you are a ${learningStyle} learner!`
        })
      };
    }

    // Content recommendations endpoint
    if (path === '/api/v1/content/recommendations/personalized' && method === 'GET') {
      const queryParams = event.queryStringParameters || {};
      const limit = parseInt(queryParams.limit) || 6;
      
      const recommendations = [
        {
          id: 1,
          title: "Introduction to Machine Learning",
          description: "Learn the fundamentals of machine learning and artificial intelligence",
          subject: "Computer Science",
          difficulty_level: "Beginner",
          duration_minutes: 45
        },
        {
          id: 2,
          title: "Web Development Fundamentals",
          description: "Master the basics of HTML, CSS, and JavaScript",
          subject: "Web Development",
          difficulty_level: "Beginner",
          duration_minutes: 60
        }
      ].slice(0, limit);

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(recommendations)
      };
    }

    // Default response
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({ 
        detail: `Endpoint not found: ${method} ${path}`,
        availableEndpoints: [
          'GET /api/v1/test',
          'POST /api/v1/users/login',
          'POST /api/v1/users/register',
          'GET /api/v1/analytics/dashboard/overview',
          'GET /api/v1/assessment/questions',
          'POST /api/v1/assessment/submit',
          'GET /api/v1/content/recommendations/personalized'
        ]
      })
    };

  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        detail: `Internal server error: ${error.message}`,
        stack: error.stack
      })
    };
  }
};
