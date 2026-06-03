# OmniMind Backend API

FastAPI-based backend for OmniMind - AI Memory Management System.

## Features

- ✅ User management (create, read, update profiles)
- ✅ Memory storage (CRUD operations with timestamps)
- ✅ Chat history management
- ✅ Knowledge graph (nodes and edges)
- ✅ Activity logging
- ✅ AI model routing rules
- ✅ Notifications system
- ✅ User statistics and analytics
- ✅ CORS enabled for frontend integration
- ✅ SQLite for development, PostgreSQL ready for production

## Installation

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create database
The database will be automatically created when the app starts. For fresh setup:
```bash
python app.py
```

## Running the Server

### Development mode (with auto-reload)
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production mode
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Setup

### SQLite (Default - Development)
The app automatically creates a SQLite database at `./omnimind.db`

### PostgreSQL (Production)
1. Install PostgreSQL
2. Create a database:
   ```sql
   CREATE DATABASE omnimind;
   ```
3. Update `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/omnimind
   ```
4. Install pgvector extension (for semantic search):
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

## API Endpoints

### Users
- `POST /api/users/` - Create user
- `GET /api/users/{user_id}` - Get user profile
- `PUT /api/users/{user_id}` - Update user profile

### Memories
- `POST /api/memories/` - Create memory
- `GET /api/memories/{user_id}` - Get all memories
- `GET /api/memories/{user_id}/{memory_id}` - Get specific memory
- `PUT /api/memories/{user_id}/{memory_id}` - Update memory
- `DELETE /api/memories/{user_id}/{memory_id}` - Delete memory

### Chat
- `POST /api/chat/{user_id}` - Save chat message
- `GET /api/chat/{user_id}` - Get chat history

### Knowledge Graph
- `POST /api/knowledge/nodes/{user_id}` - Create node
- `GET /api/knowledge/nodes/{user_id}` - Get all nodes
- `DELETE /api/knowledge/nodes/{user_id}/{node_id}` - Delete node

### Activity
- `POST /api/activity/{user_id}` - Log activity
- `GET /api/activity/{user_id}` - Get activity timeline

### AI Router
- `POST /api/router/{user_id}` - Create routing rule
- `GET /api/router/{user_id}` - Get routing rules

### Notifications
- `POST /api/notifications/{user_id}` - Create notification
- `GET /api/notifications/{user_id}` - Get notifications
- `PUT /api/notifications/{user_id}/{notif_id}/read` - Mark as read

### Stats
- `GET /api/stats/{user_id}` - Get user statistics

## Example API Calls

### Create a user
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Preeti", "email": "preeti@omnimind.io"}'
```

### Create a memory
```bash
curl -X POST "http://localhost:8000/api/memories/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Goal",
    "title": "Build OmniMind",
    "body": "Create AI memory layer",
    "tag": "Career",
    "accent": "#4d9cff"
  }'
```

### Get user stats
```bash
curl "http://localhost:8000/api/stats/1"
```

## Environment Variables

See `.env` file for configuration:
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_ORIGINS` - CORS allowed origins

## Project Structure

```
backend/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md             # This file
└── omnimind.db           # SQLite database (auto-created)
```

## Technologies

- **FastAPI** - Modern async Python web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and serialization
- **SQLite/PostgreSQL** - Database options
- **Uvicorn** - ASGI server

## Frontend Integration

The frontend is served from `../frontend/`. Both run concurrently:

```bash
# Terminal 1: Backend
cd backend && python app.py

# Terminal 2: Frontend (in another terminal)
cd frontend && python3 -m http.server 8000
```

Frontend accesses API at: `http://localhost:8000/api/*`

## Troubleshooting

### Port already in use
```bash
# Change port
python app.py --port 8001
```

### Database errors
Delete the database file and restart:
```bash
rm omnimind.db
python app.py
```

### CORS errors
Check `.env` `ALLOWED_ORIGINS` includes your frontend URL

## Future Enhancements

- [ ] JWT authentication
- [ ] pgvector for semantic search
- [ ] Redis caching
- [ ] Rate limiting
- [ ] API versioning
- [ ] Comprehensive logging
- [ ] Tests suite
- [ ] Docker containerization
