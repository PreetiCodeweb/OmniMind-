# 🚀 Quick Start - OmniMind Backend

## 1️⃣ Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## 2️⃣ Run the Backend

```bash
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 3️⃣ Test the API

Open in browser:
- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 4️⃣ Create Your First User

Using curl:
```bash
curl -X POST "http://localhost:8000/api/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Preeti", "email": "preeti@omnimind.io"}'
```

Response:
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

## 5️⃣ Create a Memory

```bash
curl -X POST "http://localhost:8000/api/memories/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Goal",
    "title": "Build OmniMind SaaS",
    "body": "Launch AI memory platform",
    "tag": "Career",
    "accent": "#4d9cff"
  }'
```

## 6️⃣ Get User Stats

```bash
curl "http://localhost:8000/api/stats/1"
```

Response shows:
- memories_stored
- sessions_synced
- knowledge_nodes
- And more...

## 📡 Connect Frontend to Backend

Update frontend API calls:
```javascript
const API_BASE = "http://localhost:8000/api";

// Example fetch
fetch(`${API_BASE}/stats/1`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## 🛑 Stop the Server

Press `Ctrl+C` in the terminal

## 🆘 Troubleshooting

**Port 8000 already in use?**
```bash
python app.py --port 8001
```

**Database errors?**
```bash
rm omnimind.db
python app.py
```

**Missing dependencies?**
```bash
pip install -r requirements.txt
```

## ✅ You're Done!

Backend is fully functional. Now connect it to your React frontend!
