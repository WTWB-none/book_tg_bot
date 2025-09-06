const { isAllowedUser } = require('./database');

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
  };

  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: '',
    };
  }

  try {
    if (event.httpMethod !== 'GET') {
      return {
        statusCode: 405,
        headers,
        body: JSON.stringify({ error: 'Method not allowed' }),
      };
    }

    // Извлекаем telegram_user_id из пути
    const pathParts = event.path.split('/');
    const telegramUserId = parseInt(pathParts[pathParts.length - 1]);

    console.log('Verify function called with path:', event.path);
    console.log('Extracted user ID:', telegramUserId);

    if (isNaN(telegramUserId)) {
      console.log('Invalid user ID:', pathParts);
      return {
        statusCode: 400,
        headers: {
          ...headers,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ error: 'Invalid user ID' }),
      };
    }

    // Проверяем локальных пользователей
    if (await isAllowedUser(telegramUserId)) {
      return {
        statusCode: 200,
        headers: {
          ...headers,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subscribed: true }),
      };
    }

    // Fallback к Tribute API
    try {
      const response = await fetch(
        process.env.TRIBUTE_API_URL,
        {
          headers: {
            'Api-Key': process.env.TRIBUTE_API_KEY,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Tribute API request failed');
      }

      const data = await response.json();
      const now = new Date();

      for (const entry of data.result || []) {
        if (entry.telegramUserId === telegramUserId) {
          if (entry.status === 'active') {
            const expireStr = entry.expireAt;
            try {
              const expireDate = new Date(expireStr);
              if (expireDate > now) {
                return {
                  statusCode: 200,
                  headers: {
                    ...headers,
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ subscribed: true }),
                };
              }
            } catch (e) {
              // Игнорируем ошибки парсинга даты
            }
          }
        }
      }

      return {
        statusCode: 200,
        headers: {
          ...headers,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subscribed: false }),
      };
    } catch (error) {
      console.error('Tribute API error:', error);
      return {
        statusCode: 200,
        headers: {
          ...headers,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subscribed: false }),
      };
    }
  } catch (error) {
    console.error('Error verifying subscription:', error);
    
    return {
      statusCode: 500,
      headers: {
        ...headers,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ error: 'Internal server error' }),
    };
  }
};
