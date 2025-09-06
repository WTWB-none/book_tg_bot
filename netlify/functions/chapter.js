const { getChapterDetail } = require('./database');

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

    // Извлекаем book_id и chapter_id из пути
    // Путь: /api/book/{book_id}/chapter/{chapter_id}
    const pathParts = event.path.split('/');
    const bookId = parseInt(pathParts[pathParts.length - 3]);
    const chapterId = parseInt(pathParts[pathParts.length - 1]);

    if (isNaN(bookId) || isNaN(chapterId)) {
      return {
        statusCode: 400,
        headers: {
          ...headers,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ error: 'Invalid book or chapter ID' }),
      };
    }

    const chapter = await getChapterDetail(bookId, chapterId);
    
    if (!chapter) {
      return {
        statusCode: 404,
        headers: {
          ...headers,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ error: 'Chapter not found' }),
      };
    }

    return {
      statusCode: 200,
      headers: {
        ...headers,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(chapter),
    };
  } catch (error) {
    console.error('Error fetching chapter:', error);
    
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
