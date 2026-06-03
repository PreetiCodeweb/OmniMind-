# 📚 Frontend-Backend Integration Guide

This guide shows how to connect your React frontend with the FastAPI backend.

## 🔗 API Service Overview

The `src/services/api.js` file contains all API functions organized by feature:

```javascript
// User Management
- createUser(name, email)
- getUser(userId)
- updateUser(userId, userData)

// Memories
- createMemory(userId, memoryData)
- getUserMemories(userId, skip, limit)
- getMemory(userId, memoryId)
- updateMemory(userId, memoryId, memoryData)
- deleteMemory(userId, memoryId)

// Chat
- saveChatMessage(userId, messageData)
- getChatHistory(userId, limit)

// Knowledge Graph
- createNode(userId, nodeData)
- getUserNodes(userId)
- deleteNode(userId, nodeId)

// Activity
- logActivity(userId, activityData)
- getUserActivity(userId, limit)

// AI Router
- createRouterRule(userId, routerData)
- getRouterRules(userId)

// Notifications
- createNotification(userId, notificationData)
- getNotifications(userId, unreadOnly)
- markNotificationAsRead(userId, notificationId)

// Stats
- getUserStats(userId)

// Health
- healthCheck()
```

## 🎯 Example: Replace Mock Data with API Calls

### Before (Using Mock Data)
```javascript
import { QUICK_STATS } from "../data.js";

export default function Dashboard() {
  return (
    <div>
      <div className="stat">
        <div className="label">Memories Stored</div>
        <div className="value">{QUICK_STATS.memoriesStored}</div>
      </div>
    </div>
  );
}
```

### After (Using Backend API)
```javascript
import { useState, useEffect } from "react";
import { getUserStats } from "../services/api.js";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const userId = 1; // Get from auth context or URL param

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await getUserStats(userId);
        setStats(data);
      } catch (error) {
        console.error("Failed to load stats:", error);
      }
    };
    fetchStats();
  }, [userId]);

  if (!stats) return <div>Loading...</div>;

  return (
    <div>
      <div className="stat">
        <div className="label">Memories Stored</div>
        <div className="value">{stats.memories_stored}</div>
      </div>
    </div>
  );
}
```

## 📝 Example: Using VaultView with Real Memories

```javascript
import { useState, useEffect } from "react";
import { getUserMemories, createMemory, deleteMemory } from "../services/api.js";

export default function VaultView() {
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const userId = 1; // From auth

  // Fetch memories on mount
  useEffect(() => {
    const fetchMemories = async () => {
      try {
        const data = await getUserMemories(userId);
        setMemories(data);
      } catch (error) {
        console.error("Error loading memories:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchMemories();
  }, [userId]);

  // Add new memory
  const handleAddMemory = async (title, body) => {
    try {
      const newMemory = await createMemory(userId, {
        type: "Goal",
        title,
        body,
        tag: "Career",
        accent: "#4d9cff",
      });
      setMemories([...memories, newMemory]);
    } catch (error) {
      console.error("Error creating memory:", error);
    }
  };

  // Delete memory
  const handleDeleteMemory = async (memoryId) => {
    try {
      await deleteMemory(userId, memoryId);
      setMemories(memories.filter((m) => m.id !== memoryId));
    } catch (error) {
      console.error("Error deleting memory:", error);
    }
  };

  if (loading) return <div>Loading memories...</div>;

  const filtered = memories.filter(
    (m) => filter === "all" || m.type === filter
  );

  if (filtered.length === 0) {
    return (
      <div className="empty-state">
        <div className="icon">🔐</div>
        <h3>No memories yet</h3>
        <p>Create your first memory to get started</p>
        <button onClick={() => handleAddMemory("New Memory", "Description")}>
          Create Memory
        </button>
      </div>
    );
  }

  return (
    <div className="vault-view">
      <div className="memory-grid">
        {filtered.map((memory) => (
          <div key={memory.id} className="memory-card">
            <h3>{memory.title}</h3>
            <p>{memory.body}</p>
            <button
              onClick={() => handleDeleteMemory(memory.id)}
              className="delete-btn"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## 💬 Example: ChatView Integration

```javascript
import { useState, useEffect } from "react";
import { getChatHistory, saveChatMessage } from "../services/api.js";

export default function ChatView() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const userId = 1;

  // Load chat history
  useEffect(() => {
    const loadChat = async () => {
      const history = await getChatHistory(userId);
      setMessages(history);
    };
    loadChat();
  }, [userId]);

  // Send message
  const handleSend = async () => {
    if (!input.trim()) return;

    try {
      // Save user message
      const userMsg = await saveChatMessage(userId, {
        role: "user",
        model: "Claude",
        text: input,
      });

      setMessages([...messages, userMsg]);
      setInput("");

      // Simulate AI response (in real app, call your AI endpoint)
      const aiMsg = await saveChatMessage(userId, {
        role: "ai",
        model: "Claude",
        text: `Response to: ${input}`,
      });

      setMessages((prev) => [...prev, aiMsg]);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div className="chat-view">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}
```

## ⚙️ Setup Instructions

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
# Backend runs on http://localhost:8000
```

### 2. Frontend Continues Using Existing Server
The frontend can run on any port. The API service automatically points to `http://localhost:8000`

### 3. Test Connection
Add this to your App.jsx to verify connection:
```javascript
import { healthCheck } from "./services/api.js";

useEffect(() => {
  healthCheck().then(status => console.log("Backend:", status));
}, []);
```

## 🔑 Key Points

1. **API_BASE** in api.js points to `http://localhost:8000/api`
2. All functions return JSON directly (already parsed)
3. Errors are caught and logged - wrap in try/catch when calling
4. userId should come from your authentication context
5. CORS is enabled on backend for all origins

## 📊 Progress

- ✅ Backend API fully implemented
- ✅ Frontend API service created
- ✅ Example integration patterns provided
- ⏭️ Next: Replace mock data with real API calls in each component

## 🚀 Next Steps

1. Update Dashboard to use `getUserStats(userId)`
2. Update VaultView to use `getUserMemories(userId)`
3. Update ChatView to use `getChatHistory(userId)`
4. Update GraphView to use `getUserNodes(userId)`
5. Add loading states and error handling
6. Implement real-time updates with WebSocket (optional)

---

Need help? Check the example functions in `src/services/api.js` for exact parameter names and return formats.
