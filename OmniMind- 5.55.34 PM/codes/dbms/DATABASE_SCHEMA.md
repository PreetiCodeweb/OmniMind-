# 📊 OmniMind Database Schema

Complete documentation of the OmniMind database structure, tables, and relationships.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Database Tables](#database-tables)
3. [Relationships](#relationships)
4. [Data Types](#data-types)
5. [Indexes](#indexes)
6. [Sample Data](#sample-data)

---

## Overview

The OmniMind database is designed to support an AI-powered memory management system with features for:
- User account management
- Memory storage and retrieval
- Chat history tracking
- Knowledge graph management
- Activity logging
- AI model routing
- Notifications

**Database Options:**
- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)

---

## Database Tables

### 1. **users** - User Accounts
Stores user profile information and statistics.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique user identifier |
| name | VARCHAR(255) | NOT NULL | User's full name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| tier | VARCHAR(50) | DEFAULT 'Free' | Subscription tier (Free, Pro, Enterprise) |
| avatar | VARCHAR(10) | DEFAULT 'P' | User's avatar character |
| total_sessions | INTEGER | DEFAULT 0 | Total chat sessions count |
| streak | INTEGER | DEFAULT 0 | Current activity streak (days) |
| created_at | TIMESTAMP | DEFAULT NOW | Account creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW | Last profile update |

**Sample Data:**
- 4 users with different tiers (Free, Pro, Enterprise)
- Streaks ranging from 2 to 12 days
- Email validation ensures unique accounts

---

### 2. **memories** - User Memories
Stores user's saved memories with categorization and metadata.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique memory identifier |
| user_id | INTEGER | FK → users(id) | Owner of the memory |
| type | VARCHAR(50) | NOT NULL | Memory type (Goal, Project, Skill, Decision, Research, Preference) |
| title | VARCHAR(255) | NOT NULL | Memory title |
| body | TEXT | NOT NULL | Memory content/description |
| tag | VARCHAR(50) | | Category tag (Career, Learning, Technical, Personal, Research) |
| accent | VARCHAR(20) | | Color code (#RRGGBB) for UI display |
| created_at | TIMESTAMP | DEFAULT NOW | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW | Last modification time |

**Memory Types:**
- `Goal` - Personal or professional goals
- `Project` - Active projects
- `Skill` - Skills to learn or improve
- `Decision` - Important decisions made
- `Research` - Research topics and findings
- `Preference` - Personal preferences

**Sample Data:**
- 15 memories across 4 users
- Mixed types: Goals, Projects, Skills, Research, Decisions
- Color-coded for visual organization

---

### 3. **chat_messages** - Chat History
Stores all chat messages between users and AI models.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique message identifier |
| user_id | INTEGER | FK → users(id) | Message author |
| role | VARCHAR(10) | NOT NULL | 'user' or 'ai' |
| model | VARCHAR(50) | | AI model used (Claude, GPT-4o, Gemini, Grok, Mistral) |
| text | TEXT | NOT NULL | Message content |
| created_at | TIMESTAMP | DEFAULT NOW | Message timestamp |

**Sample Data:**
- 10 chat messages demonstrating user-AI interactions
- Messages from multiple users
- Tracks which model was used for each response

---

### 4. **knowledge_nodes** - Graph Nodes
Represents nodes in user's knowledge graph.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique node identifier |
| user_id | INTEGER | FK → users(id) | Node owner |
| label | VARCHAR(255) | NOT NULL | Node label/title |
| type | VARCHAR(50) | | Node type (root, main, sub) |
| color | VARCHAR(20) | | Hex color code for visualization |
| x | FLOAT | | X coordinate for graph layout |
| y | FLOAT | | Y coordinate for graph layout |
| r | FLOAT | | Radius for node visualization |
| created_at | TIMESTAMP | DEFAULT NOW | Creation time |

**Node Types:**
- `root` - Central/main concept (largest size)
- `main` - Primary related concepts
- `sub` - Sub-concepts or details

**Sample Data:**
- 17 knowledge nodes creating 4 different knowledge graphs
- Positioned with x, y coordinates for visualization
- Color-coded by topic

---

### 5. **knowledge_edges** - Graph Connections
Defines relationships between knowledge nodes.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique edge identifier |
| user_id | INTEGER | FK → users(id) | Edge owner |
| from_node_id | INTEGER | NOT NULL | Source node ID |
| to_node_id | INTEGER | NOT NULL | Target node ID |
| created_at | TIMESTAMP | DEFAULT NOW | Creation time |

**Sample Data:**
- Connections between root, main, and sub nodes
- Forms hierarchical knowledge structures
- Example: OmniMind → Backend → FastAPI

---

### 6. **activity_logs** - Activity History
Tracks user actions for audit and timeline purposes.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique log entry ID |
| user_id | INTEGER | FK → users(id) | User performing action |
| action | VARCHAR(100) | | Action type (Created, Updated, Deleted, Shared, Started) |
| object_type | VARCHAR(50) | | What was acted upon (Memory, ChatSession, KnowledgeNode, Project) |
| object_name | VARCHAR(255) | | Name of the object |
| status | VARCHAR(50) | DEFAULT 'completed' | Status (completed, pending, failed, in_progress) |
| created_at | TIMESTAMP | DEFAULT NOW | Action timestamp |

**Sample Data:**
- 11 activity logs showing user interactions
- Mix of completed, pending, and in-progress statuses
- Tracks memory creation, updates, and project work

---

### 7. **model_routers** - AI Model Routing Rules
Stores user preferences for routing tasks to specific AI models.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique rule identifier |
| user_id | INTEGER | FK → users(id) | Rule owner |
| task | VARCHAR(100) | | Task type (Code Review, Documentation, Analysis, etc.) |
| model | VARCHAR(100) | | Preferred AI model |
| reason | TEXT | | Why this model is preferred |
| active | BOOLEAN | DEFAULT 1 | Whether rule is active |
| created_at | TIMESTAMP | DEFAULT NOW | Creation time |

**Sample Data:**
- 10 routing rules across different users
- Examples: Code Review → Claude, Documentation → GPT-4o
- Each rule has explanation for the choice

---

### 8. **notifications** - User Notifications
Stores notifications and alerts for users.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique notification ID |
| user_id | INTEGER | FK → users(id) | Notification recipient |
| type | VARCHAR(20) | | Type (success, warning, info, error) |
| message | VARCHAR(255) | | Notification message |
| icon | VARCHAR(10) | | Icon/emoji to display |
| read | BOOLEAN | DEFAULT 0 | Read status |
| created_at | TIMESTAMP | DEFAULT NOW | Creation timestamp |

**Notification Types:**
- `success` - Operation successful (✓)
- `warning` - Warning/attention needed (⚠)
- `info` - Information/news (ℹ)
- `error` - Error occurred (✗)

**Sample Data:**
- 10 notifications with mixed types
- Both read and unread notifications
- Real examples: memory saved, storage limit warning, model availability

---

## Relationships

```
┌─────────────┐
│   users     │
└──────┬──────┘
       │
       ├─────→ memories
       ├─────→ chat_messages
       ├─────→ knowledge_nodes
       ├─────→ knowledge_edges
       ├─────→ activity_logs
       ├─────→ model_routers
       └─────→ notifications

knowledge_nodes ←─────→ knowledge_edges
  (1 user)                (same user)
```

### Foreign Key Relationships

1. **memories** → **users**
   - `memories.user_id` → `users.id`
   - ON DELETE: CASCADE (delete user's memories)

2. **chat_messages** → **users**
   - `chat_messages.user_id` → `users.id`
   - ON DELETE: CASCADE (delete user's messages)

3. **knowledge_nodes** → **users**
   - `knowledge_nodes.user_id` → `users.id`
   - ON DELETE: CASCADE (delete user's nodes)

4. **knowledge_edges** → **users**
   - `knowledge_edges.user_id` → `users.id`
   - ON DELETE: CASCADE (delete user's edges)

5. **activity_logs** → **users**
   - `activity_logs.user_id` → `users.id`
   - ON DELETE: CASCADE (delete user's activities)

6. **model_routers** → **users**
   - `model_routers.user_id` → `users.id`
   - ON DELETE: CASCADE (delete user's routing rules)

7. **notifications** → **users**
   - `notifications.user_id` → `users.id`
   - ON DELETE: CASCADE (delete user's notifications)

---

## Data Types

### SQL Data Types Used

| Type | Usage | Examples |
|------|-------|----------|
| INTEGER | IDs, counts, coordinates | id, total_sessions, x, y |
| VARCHAR(n) | Short text fields | name, email, tag, model |
| TEXT | Long text content | body (memory), reason (router), text (chat) |
| TIMESTAMP | Date/time tracking | created_at, updated_at |
| BOOLEAN | Binary flags | active, read |
| FLOAT | Decimal coordinates | x, y, r (graph positioning) |

### Format Conventions

- **Email**: Standard email format (validated by Pydantic)
- **Colors**: Hex format (#RRGGBB) - e.g., #4d9cff
- **Coordinates**: Float values for graph positioning
- **Timestamps**: ISO 8601 format with UTC timezone

---

## Indexes

Performance optimization indexes created:

```sql
CREATE INDEX idx_memories_user_id ON memories(user_id);
CREATE INDEX idx_memories_created_at ON memories(created_at);
CREATE INDEX idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX idx_knowledge_nodes_user_id ON knowledge_nodes(user_id);
CREATE INDEX idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
```

**Index Strategy:**
- User ID indexing for fast filtering by user
- Timestamp indexing for chronological queries
- Improves query performance on large datasets

---

## Sample Data

### Users (4 records)
| Name | Email | Tier | Sessions | Streak |
|------|-------|------|----------|--------|
| Preeti Sasmal | preeti@omnimind.io | Pro | 24 | 7 |
| Alice Chen | alice@omnimind.io | Free | 5 | 2 |
| Bob Johnson | bob@omnimind.io | Pro | 18 | 5 |
| Sarah Williams | sarah@omnimind.io | Enterprise | 42 | 12 |

### Data Summary
- **15 Memories** - Goals, Projects, Skills, Research, Decisions
- **10 Chat Messages** - Multi-turn conversations with different models
- **17 Knowledge Nodes** - 4 separate knowledge graphs
- **11 Activity Logs** - User action history
- **10 Model Routers** - AI model routing preferences
- **10 Notifications** - Mixed types and read status

### Total Records
- **67 sample data records** for development and testing

---

## Querying Examples

### Get user's memories by type
```sql
SELECT * FROM memories 
WHERE user_id = 1 AND type = 'Goal'
ORDER BY created_at DESC;
```

### Get recent chat history
```sql
SELECT * FROM chat_messages 
WHERE user_id = 1 
ORDER BY created_at DESC 
LIMIT 20;
```

### Get user's knowledge graph
```sql
SELECT * FROM knowledge_nodes 
WHERE user_id = 1 
ORDER BY type DESC;
```

### Get activity timeline
```sql
SELECT * FROM activity_logs 
WHERE user_id = 1 
ORDER BY created_at DESC 
LIMIT 10;
```

### Get unread notifications
```sql
SELECT * FROM notifications 
WHERE user_id = 1 AND read = 0 
ORDER BY created_at DESC;
```

---

## Initialization

### Using Python Script
```bash
cd codes/dbms
python init_db.py
```

### Manual SQL Import
```bash
sqlite3 omnimind.db < schema.sql < seed_data.sql
```

### With FastAPI App
```bash
cd codes/backend
python app.py
# Database auto-initializes on first run
```

---

## Maintenance

### Backup Database
```bash
# SQLite
cp omnimind.db omnimind.db.backup

# PostgreSQL
pg_dump omnimind > backup.sql
```

### Reset Database
```bash
rm omnimind.db
python init_db.py
```

### Monitor Database Size
```bash
# SQLite
ls -lh omnimind.db

# PostgreSQL
SELECT pg_size_pretty(pg_database_size('omnimind'));
```

---

## Performance Tips

1. **Use Indexes**: All frequently queried columns are indexed
2. **Pagination**: Use LIMIT/OFFSET for large result sets
3. **Batch Operations**: Insert multiple records in one transaction
4. **Connection Pooling**: FastAPI uses connection pooling by default
5. **Query Optimization**: Use specific SELECT columns, not SELECT *

---

## Future Enhancements

- [ ] Vector embeddings table for semantic search
- [ ] Full-text search indexing
- [ ] Audit logging for changes
- [ ] Soft deletes (is_deleted flag)
- [ ] Database versioning/migrations
- [ ] Data anonymization for exports
- [ ] Automated backups schedule
- [ ] Performance monitoring queries

---

**Last Updated**: June 2, 2024
**Database Version**: 1.0
**Status**: ✅ Production Ready
