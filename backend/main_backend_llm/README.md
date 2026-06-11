# OmniMind LLM Backend

A production-ready Node.js/Express backend that powers OmniMind's chat system with real LLM responses (Claude or GPT-4), conversation history, JWT auth, and SSE streaming.

---

## Folder Structure

```
backend/
├── config/
│   ├── db.js                  # MongoDB connection
│   └── llm.config.js          # LLM model settings & system prompt
├── controllers/
│   ├── auth.controller.js     # Register, login, profile
│   ├── chat.controller.js     # Send/stream chat messages
│   └── conversation.controller.js  # CRUD for conversations
├── middleware/
│   ├── auth.middleware.js     # JWT protect + role guard
│   ├── errorHandler.js        # Global error handler
│   ├── rateLimiter.js         # Rate limiting per route type
│   └── validate.middleware.js # Input validation rules
├── models/
│   ├── user.model.js          # User schema
│   └── conversation.model.js  # Conversation + messages schema
├── routes/
│   ├── auth.routes.js
│   ├── chat.routes.js
│   └── conversation.routes.js
├── services/
│   ├── llm.service.js         # Core LLM calls (Anthropic + OpenAI)
│   └── chat.service.js        # Conversation management + LLM orchestration
├── utils/
│   ├── ApiError.js            # Structured HTTP error class
│   └── catchAsync.js          # Async error wrapper
├── .env.example
├── .gitignore
├── package.json
└── server.js                  # Entry point
```

---

## Quick Setup

### 1. Install dependencies
```bash
cd backend
npm install
```

### 2. Configure environment
```bash
cp .env.example .env
```

Edit `.env` and fill in:
- `MONGO_URI` — your MongoDB connection string
- `JWT_SECRET` — a long random secret
- `ANTHROPIC_API_KEY` — from console.anthropic.com  
- `LLM_PROVIDER` — `anthropic` (default) or `openai`

### 3. Run
```bash
# Development (with auto-reload)
npm run dev

# Production
npm start
```

Server starts on `http://localhost:5000`

---

## API Reference

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register` | No | Create account |
| POST | `/api/auth/login` | No | Login, get JWT |
| GET | `/api/auth/me` | Yes | Get current user |
| PATCH | `/api/auth/me` | Yes | Update name/avatar |

**Register body:**
```json
{ "name": "Preeti", "email": "p@example.com", "password": "secret123" }
```

**Login response:**
```json
{ "success": true, "token": "eyJ...", "user": { "id": "...", "name": "Preeti", ... } }
```

---

### Chat

All chat routes require `Authorization: Bearer <token>` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Standard response (wait for full reply) |
| POST | `/api/chat/stream` | Streaming SSE response (ChatGPT-style) |

**Request body (both):**
```json
{
  "message": "What is the meaning of life?",
  "conversationId": "optional-existing-id"
}
```

**Standard response:**
```json
{
  "success": true,
  "conversationId": "664abc...",
  "title": "What is the meaning of life?",
  "message": { "role": "assistant", "content": "42, obviously...", "tokens": 120 }
}
```

**Stream response (SSE events):**
```
data: {"type":"start","conversationId":"664abc..."}
data: {"type":"chunk","content":"The "}
data: {"type":"chunk","content":"meaning "}
data: {"type":"chunk","content":"of life..."}
data: {"type":"done"}
```

---

### Conversations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/conversations` | List all conversations |
| GET | `/api/conversations/:id` | Get conversation with messages |
| DELETE | `/api/conversations/:id` | Delete conversation |
| DELETE | `/api/conversations` | Delete all conversations |
| PATCH | `/api/conversations/:id/title` | Rename conversation |
| PATCH | `/api/conversations/:id/pin` | Toggle pin |
| PATCH | `/api/conversations/:id/archive` | Toggle archive |

---

## Frontend Integration (React example)

### Standard chat
```js
const response = await fetch("/api/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify({ message, conversationId })
});
const data = await response.json();
// data.message.content  ← AI reply
// data.conversationId   ← use for follow-up messages
```

### Streaming chat (ChatGPT-style)
```js
const response = await fetch("/api/chat/stream", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify({ message, conversationId })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const lines = decoder.decode(value).split("\n");
  for (const line of lines) {
    if (!line.startsWith("data: ")) continue;
    const event = JSON.parse(line.slice(6));

    if (event.type === "start") setConversationId(event.conversationId);
    if (event.type === "chunk") setReply(prev => prev + event.content);
    if (event.type === "done") setIsStreaming(false);
  }
}
```

---

## Switching LLM Provider

In `.env`, change `LLM_PROVIDER`:
- `anthropic` → uses Claude (recommended)
- `openai` → uses GPT-4o

Change model name via `ANTHROPIC_MODEL` or `OPENAI_MODEL`.

---

## Customizing the AI Persona

Edit in `.env`:
```
AI_NAME=OmniMind
AI_PERSONA=You are OmniMind, a highly intelligent AI assistant built by Preeti...
```
