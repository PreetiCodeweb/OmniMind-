# 🗄️ Database Quick Reference

Fast lookup guide for OmniMind database operations.

## Files in This Directory

| File | Purpose | Size |
|------|---------|------|
| `schema.sql` | Database table definitions | ~2.5 KB |
| `seed_data.sql` | Sample data for all tables | ~8 KB |
| `init_db.py` | Python initialization script | ~9 KB |
| `DATABASE_SCHEMA.md` | Complete schema documentation | Detailed reference |
| `README.md` | This quick reference | Quick lookup |

## Quick Commands

### Initialize Database

**Using Python script (recommended):**
```bash
python init_db.py
```

**Using SQL files:**
```bash
sqlite3 omnimind.db < schema.sql < seed_data.sql
```

### Database Locations

```
Development: ./omnimind.db (SQLite)
Production: postgresql://user:password@host/omnimind
```

## Table Count Summary

| Table | Records | Purpose |
|-------|---------|---------|
| users | 4 | User accounts |
| memories | 15 | Saved memories |
| chat_messages | 10 | Conversation history |
| knowledge_nodes | 17 | Graph nodes |
| knowledge_edges | 7 | Node connections |
| activity_logs | 11 | Action history |
| model_routers | 10 | AI routing rules |
| notifications | 10 | User alerts |
| **TOTAL** | **84** | **Complete dataset** |

## Sample Users

```
ID  Name                Email                    Tier        Sessions
1   Preeti Sasmal       preeti@omnimind.io      Pro         24
2   Alice Chen          alice@omnimind.io       Free        5
3   Bob Johnson         bob@omnimind.io         Pro         18
4   Sarah Williams      sarah@omnimind.io       Enterprise  42
```

## Common Queries

### Get all memories for user
```sql
SELECT * FROM memories WHERE user_id = 1;
```

### Count memories by type
```sql
SELECT type, COUNT(*) FROM memories GROUP BY type;
```

### Get recent chats
```sql
SELECT * FROM chat_messages WHERE user_id = 1 ORDER BY created_at DESC LIMIT 10;
```

### Get user stats
```sql
SELECT 
  (SELECT COUNT(*) FROM memories WHERE user_id = 1) as memory_count,
  (SELECT COUNT(*) FROM chat_messages WHERE user_id = 1) as chat_count,
  (SELECT COUNT(*) FROM knowledge_nodes WHERE user_id = 1) as node_count;
```

### Get unread notifications
```sql
SELECT * FROM notifications WHERE user_id = 1 AND read = 0;
```

### Mark notification as read
```sql
UPDATE notifications SET read = 1 WHERE id = 1;
```

## Memory Types

- `Goal` - Professional/personal goals
- `Project` - Active projects
- `Skill` - Skills to learn
- `Decision` - Important decisions
- `Research` - Research findings
- `Preference` - Personal preferences

## Notification Types

- `success` - ✓ Operation successful
- `warning` - ⚠ Warning/caution
- `info` - ℹ Information
- `error` - ✗ Error occurred

## Color Codes (Used in UI)

- `#4d9cff` - Primary blue
- `#7c3aed` - Purple
- `#06b6d4` - Cyan
- `#f59e0b` - Amber
- `#8b5cf6` - Violet
- `#ec4899` - Pink

## Database Environment Variables

```env
DATABASE_URL=sqlite:///./omnimind.db
# Or PostgreSQL:
DATABASE_URL=postgresql://user:password@localhost/omnimind
```

## Performance Tips

- ✅ Indexes on user_id for fast lookups
- ✅ Timestamp indexes for chronological queries
- ✅ Use pagination for large result sets
- ✅ Connection pooling enabled in FastAPI

## Data Relationships

```
users (1) ──→ (many) memories
users (1) ──→ (many) chat_messages
users (1) ──→ (many) knowledge_nodes
users (1) ──→ (many) knowledge_edges
users (1) ──→ (many) activity_logs
users (1) ──→ (many) model_routers
users (1) ──→ (many) notifications
```

All relationships cascade on user deletion.

## Testing Data

Sample queries to verify database setup:

```sql
-- Count total records
SELECT COUNT(*) FROM users;        -- Should be 4
SELECT COUNT(*) FROM memories;     -- Should be 15
SELECT COUNT(*) FROM chat_messages; -- Should be 10

-- Get sample data
SELECT * FROM users LIMIT 1;
SELECT * FROM memories WHERE user_id = 1 LIMIT 1;
SELECT * FROM knowledge_nodes WHERE user_id = 1 LIMIT 1;
```

## Troubleshooting

**Database file exists but won't open:**
```bash
sqlite3 omnimind.db ".tables"
```

**Need to reset database:**
```bash
rm omnimind.db
python init_db.py
```

**Check database size:**
```bash
ls -lh omnimind.db
```

## Backup & Restore

### Backup SQLite
```bash
cp omnimind.db omnimind.db.backup
```

### Backup PostgreSQL
```bash
pg_dump omnimind > backup.sql
```

### Restore PostgreSQL
```bash
psql omnimind < backup.sql
```

## Connection Strings

**SQLite (Development):**
```
sqlite:///./omnimind.db
```

**PostgreSQL (Production):**
```
postgresql://username:password@localhost:5432/omnimind
```

**With SQLAlchemy in Python:**
```python
from sqlalchemy import create_engine
engine = create_engine("sqlite:///./omnimind.db")
```

## API Endpoint Examples

See `backend/API_TESTING.md` for detailed API testing examples with cURL commands.

## Next Steps

1. ✅ Initialize database with `python init_db.py`
2. ✅ Verify with sample queries above
3. ✅ Connect backend to database
4. ✅ Connect frontend to API endpoints
5. ✅ Test with seed data

---

**Database Status**: ✅ Ready for development and testing
**Last Updated**: June 2, 2024
