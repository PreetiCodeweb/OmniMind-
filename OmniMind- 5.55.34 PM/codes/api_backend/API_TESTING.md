# 🧪 API Testing Guide - cURL Commands

Quick reference for testing all backend endpoints using cURL commands.

## 🏥 Health Check

```bash
# Check if backend is running
curl http://localhost:8000/health
curl http://localhost:8000/
```

---

## 👤 User Management

### Create User
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Preeti", "email": "preeti@omnimind.io"}'
```

**Response:**
```json
{
  "id": 1,
  "name": "Preeti",
  "email": "preeti@omnimind.io",
  "tier": "Free",
  "avatar": "P",
  "total_sessions": 0,
  "streak": 0,
  "created_at": "2024-06-02T22:10:00"
}
```

### Get User
```bash
curl http://localhost:8000/api/users/1
```

### Update User
```bash
curl -X PUT "http://localhost:8000/api/users/1" \
  -H "Content-Type: application/json" \
  -d '{"tier": "Pro", "total_sessions": 5, "streak": 3}'
```

---

## 💾 Memories

### Create Memory
```bash
curl -X POST "http://localhost:8000/api/memories/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Goal",
    "title": "Build OmniMind SaaS",
    "body": "Launch AI memory management platform",
    "tag": "Career",
    "accent": "#4d9cff"
  }'
```

### Get All Memories
```bash
curl http://localhost:8000/api/memories/1
curl http://localhost:8000/api/memories/1?skip=0&limit=50
```

### Get Single Memory
```bash
curl http://localhost:8000/api/memories/1/1
```

### Update Memory
```bash
curl -X PUT "http://localhost:8000/api/memories/1/1" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Goal",
    "title": "Updated Title",
    "body": "Updated content",
    "tag": "Career",
    "accent": "#ff6b6b"
  }'
```

### Delete Memory
```bash
curl -X DELETE "http://localhost:8000/api/memories/1/1"
```

---

## 💬 Chat Messages

### Save Chat Message
```bash
curl -X POST "http://localhost:8000/api/chat/1" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "model": "Claude",
    "text": "How do I organize my thoughts?"
  }'
```

### Get Chat History
```bash
curl http://localhost:8000/api/chat/1
curl http://localhost:8000/api/chat/1?limit=20
```

---

## 🧠 Knowledge Graph

### Create Node
```bash
curl -X POST "http://localhost:8000/api/knowledge/nodes/1" \
  -H "Content-Type: application/json" \
  -d '{
    "label": "AI Concepts",
    "type": "main",
    "color": "#4d9cff",
    "x": 100,
    "y": 150,
    "r": 50
  }'
```

### Get All Nodes
```bash
curl http://localhost:8000/api/knowledge/nodes/1
```

### Delete Node
```bash
curl -X DELETE "http://localhost:8000/api/knowledge/nodes/1/1"
```

---

## 📋 Activity Logging

### Log Activity
```bash
curl -X POST "http://localhost:8000/api/activity/1" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "Created",
    "object_type": "Memory",
    "object_name": "OmniMind Goals",
    "status": "completed"
  }'
```

### Get Activity Timeline
```bash
curl http://localhost:8000/api/activity/1
curl http://localhost:8000/api/activity/1?limit=10
```

---

## 🤖 AI Router Rules

### Create Router Rule
```bash
curl -X POST "http://localhost:8000/api/router/1" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analysis",
    "model": "Claude",
    "reason": "Best for detailed analysis",
    "active": true
  }'
```

### Get Router Rules
```bash
curl http://localhost:8000/api/router/1
```

---

## 🔔 Notifications

### Create Notification
```bash
curl -X POST "http://localhost:8000/api/notifications/1" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "success",
    "message": "Memory saved successfully!",
    "icon": "✓"
  }'
```

### Get Notifications
```bash
curl http://localhost:8000/api/notifications/1
curl http://localhost:8000/api/notifications/1?unread_only=false
```

### Mark as Read
```bash
curl -X PUT "http://localhost:8000/api/notifications/1/1/read"
```

---

## 📊 Statistics

### Get User Stats
```bash
curl http://localhost:8000/api/stats/1
```

**Response:**
```json
{
  "user_id": 1,
  "memories_stored": 5,
  "sessions_synced": 3,
  "knowledge_nodes": 12,
  "chat_messages": 28,
  "hours_saved": 38,
  "accuracy_rate": 94.2,
  "response_time": 340
}
```

---

## 🔗 Bulk Operations - Example Workflow

### Complete User Journey
```bash
# 1. Create user
USER=$(curl -s -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@omnimind.io"}' | grep -o '"id":[0-9]*' | cut -d: -f2)

echo "Created user ID: $USER"

# 2. Create memory
MEMORY=$(curl -s -X POST "http://localhost:8000/api/memories/?user_id=$USER" \
  -H "Content-Type: application/json" \
  -d '{"type": "Goal", "title": "Learn FastAPI", "body": "Master backend development", "tag": "Learning", "accent": "#4d9cff"}' | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)

echo "Created memory ID: $MEMORY"

# 3. Log activity
curl -s -X POST "http://localhost:8000/api/activity/$USER" \
  -H "Content-Type: application/json" \
  -d '{"action": "Created", "object_type": "Memory", "object_name": "Learn FastAPI", "status": "completed"}' > /dev/null

# 4. Create chat message
curl -s -X POST "http://localhost:8000/api/chat/$USER" \
  -H "Content-Type: application/json" \
  -d '{"role": "user", "model": "Claude", "text": "How do I get started with FastAPI?"}' > /dev/null

# 5. Get user stats
echo "Final stats:"
curl -s "http://localhost:8000/api/stats/$USER" | jq '.'
```

---

## 📝 Testing Tips

### Pretty Print JSON
```bash
curl http://localhost:8000/api/users/1 | jq '.'
```

### Save Response to File
```bash
curl http://localhost:8000/api/stats/1 > stats.json
```

### Check Response Headers
```bash
curl -i http://localhost:8000/api/users/1
```

### Measure Request Time
```bash
curl -w "\n%{time_total}s\n" http://localhost:8000/api/users/1
```

### Send Multiline JSON
```bash
curl -X POST "http://localhost:8000/api/memories/?user_id=1" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF'
{
  "type": "Project",
  "title": "OmniMind",
  "body": "Build an AI-powered memory management system",
  "tag": "Personal",
  "accent": "#4d9cff"
}
EOF
```

---

## 🐛 Common Issues

**Port already in use?**
```bash
# Change port in backend
python app.py --port 8001
# Update API_BASE in frontend to http://localhost:8001/api
```

**CORS Error?**
Backend has CORS enabled for all origins, but verify by:
```bash
curl -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: POST" http://localhost:8000/api/users/
```

**Database Error?**
```bash
# Reset database
rm omnimind.db
python app.py
```

---

## 📚 API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These show interactive API documentation with "Try it out" buttons!

---

## 🚀 Automation Script Example

Save as `test_api.sh`:
```bash
#!/bin/bash
BASE_URL="http://localhost:8000/api"
USER_ID=1

echo "🧪 Testing OmniMind API..."

echo "✓ Creating user..."
curl -s -X POST "$BASE_URL/users/" -H "Content-Type: application/json" -d '{"name": "Test", "email": "test@example.com"}' | jq .

echo "✓ Getting user..."
curl -s "$BASE_URL/users/$USER_ID" | jq .

echo "✓ Getting stats..."
curl -s "$BASE_URL/stats/$USER_ID" | jq .

echo "✅ API tests complete!"
```

Run with: `bash test_api.sh`

---

**Need more examples?** Check the integration guide at `frontend/INTEGRATION_GUIDE.md`
