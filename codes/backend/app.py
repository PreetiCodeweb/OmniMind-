from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
import os
from pathlib import Path
import subprocess
import sys
import time
from dotenv import load_dotenv

load_dotenv()

# ============ DATABASE SETUP ============
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# For SQLite (development)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# For PostgreSQL (production)
else:
    engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============ DATABASE MODELS ============
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    tier = Column(String(50), default="Free")
    avatar = Column(String(10), default="P")
    total_sessions = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Memory(Base):
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    type = Column(String(50))  # Goal, Project, Skill, Preference, Research, Decision
    title = Column(String(255))
    body = Column(Text)
    tag = Column(String(50))
    accent = Column(String(20))  # Color code
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    role = Column(String(10))  # "user" or "ai"
    model = Column(String(50))  # Claude, GPT-4o, Gemini, etc.
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class KnowledgeNode(Base):
    __tablename__ = "knowledge_nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    label = Column(String(255))
    type = Column(String(50))  # root, main, sub
    color = Column(String(20))
    x = Column(Float)
    y = Column(Float)
    r = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeEdge(Base):
    __tablename__ = "knowledge_edges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    from_node_id = Column(Integer)
    to_node_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    action = Column(String(100))  # Created, Updated, Shared, etc.
    object_type = Column(String(50))  # Memory, ChatSession, Node, etc.
    object_name = Column(String(255))
    status = Column(String(50), default="completed")  # completed, pending, failed
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class ModelRouter(Base):
    __tablename__ = "model_routers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    task = Column(String(100))
    model = Column(String(100))
    reason = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    type = Column(String(20))  # success, warning, info
    message = Column(String(255))
    icon = Column(String(10))
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# ============ PYDANTIC SCHEMAS ============
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    tier: str
    avatar: str
    total_sessions: int
    streak: int
    created_at: datetime

    class Config:
        from_attributes = True

class MemoryCreate(BaseModel):
    type: str
    title: str
    body: str
    tag: str
    accent: str

class MemoryResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    body: str
    tag: str
    accent: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatMessageCreate(BaseModel):
    role: str
    model: str
    text: str

class ChatMessageResponse(BaseModel):
    id: int
    user_id: int
    role: str
    model: str
    text: str
    created_at: datetime

    class Config:
        from_attributes = True

class KnowledgeNodeCreate(BaseModel):
    label: str
    type: str
    color: str
    x: float
    y: float
    r: float

class KnowledgeNodeResponse(BaseModel):
    id: int
    label: str
    type: str
    color: str
    x: float
    y: float
    r: float

    class Config:
        from_attributes = True

class ActivityLogResponse(BaseModel):
    id: int
    action: str
    object_type: str
    object_name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    id: int
    type: str
    message: str
    icon: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ============ FASTAPI APP ============
app = FastAPI(
    title="OmniMind API",
    description="Backend API for OmniMind - AI Memory Management System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CYBER_RUNNER_FILE = PROJECT_ROOT / "games" / "cyber_runner.py"
CYBER_RUNNER_LOG = PROJECT_ROOT / "games" / "cyber_runner.log"
AI_SPACE_DEFENDER_FILE = PROJECT_ROOT / "games" / "ai_space_defender.py"
AI_SPACE_DEFENDER_LOG = PROJECT_ROOT / "games" / "ai_space_defender.log"
BRAIN_CHALLENGE_FILE = PROJECT_ROOT / "games" / "brain_challenge.py"
BRAIN_CHALLENGE_LOG = PROJECT_ROOT / "games" / "brain_challenge.log"
cyber_runner_process = None
ai_space_defender_process = None
brain_challenge_process = None

# ============ API ROUTES ============

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {"message": "OmniMind API v1.0.0", "status": "online"}

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# ============ GAME ROUTES ============
@app.post("/api/games/cyber-runner/start", tags=["Games"])
async def start_cyber_runner():
    """Start the local Cyber Runner Pygame script."""
    global cyber_runner_process

    if not CYBER_RUNNER_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Game file not found: {CYBER_RUNNER_FILE}",
        )

    if cyber_runner_process and cyber_runner_process.poll() is None:
        return {"status": "already_running", "file": str(CYBER_RUNNER_FILE)}

    try:
        with CYBER_RUNNER_LOG.open("w") as log_file:
            cyber_runner_process = subprocess.Popen(
                [sys.executable, str(CYBER_RUNNER_FILE)],
                cwd=str(CYBER_RUNNER_FILE.parent),
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not start game: {exc}")

    time.sleep(0.6)
    if cyber_runner_process.poll() is not None:
        log_text = CYBER_RUNNER_LOG.read_text(errors="replace")[-2000:]
        raise HTTPException(
            status_code=500,
            detail=f"Cyber Runner exited immediately. {log_text}".strip(),
        )

    return {
        "status": "started",
        "pid": cyber_runner_process.pid,
        "file": str(CYBER_RUNNER_FILE),
        "log": str(CYBER_RUNNER_LOG),
    }

@app.post("/api/games/ai-space-defender/start", tags=["Games"])
async def start_ai_space_defender():
    """Start the local AI Space Defender Pygame script."""
    global ai_space_defender_process

    if not AI_SPACE_DEFENDER_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Game file not found: {AI_SPACE_DEFENDER_FILE}",
        )

    if ai_space_defender_process and ai_space_defender_process.poll() is None:
        return {"status": "already_running", "file": str(AI_SPACE_DEFENDER_FILE)}

    try:
        with AI_SPACE_DEFENDER_LOG.open("w") as log_file:
            ai_space_defender_process = subprocess.Popen(
                [sys.executable, str(AI_SPACE_DEFENDER_FILE)],
                cwd=str(AI_SPACE_DEFENDER_FILE.parent),
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not start game: {exc}")

    time.sleep(0.6)
    if ai_space_defender_process.poll() is not None:
        log_text = AI_SPACE_DEFENDER_LOG.read_text(errors="replace")[-2000:]
        raise HTTPException(
            status_code=500,
            detail=f"AI Space Defender exited immediately. {log_text}".strip(),
        )

    return {
        "status": "started",
        "pid": ai_space_defender_process.pid,
        "file": str(AI_SPACE_DEFENDER_FILE),
        "log": str(AI_SPACE_DEFENDER_LOG),
    }

@app.post("/api/games/brain-challenge/start", tags=["Games"])
async def start_brain_challenge():
    """Start the local Brain Challenge Pygame script."""
    global brain_challenge_process

    if not BRAIN_CHALLENGE_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Game file not found: {BRAIN_CHALLENGE_FILE}",
        )

    if brain_challenge_process and brain_challenge_process.poll() is None:
        return {"status": "already_running", "file": str(BRAIN_CHALLENGE_FILE)}

    try:
        with BRAIN_CHALLENGE_LOG.open("w") as log_file:
            brain_challenge_process = subprocess.Popen(
                [sys.executable, str(BRAIN_CHALLENGE_FILE)],
                cwd=str(BRAIN_CHALLENGE_FILE.parent),
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not start game: {exc}")

    time.sleep(0.6)
    if brain_challenge_process.poll() is not None:
        log_text = BRAIN_CHALLENGE_LOG.read_text(errors="replace")[-2000:]
        raise HTTPException(
            status_code=500,
            detail=f"Brain Challenge exited immediately. {log_text}".strip(),
        )

    return {
        "status": "started",
        "pid": brain_challenge_process.pid,
        "file": str(BRAIN_CHALLENGE_FILE),
        "log": str(BRAIN_CHALLENGE_LOG),
    }

# ============ USER ROUTES ============
@app.post("/api/users/", response_model=UserResponse, tags=["Users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/api/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    """Update user profile"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in user_data.items():
        if hasattr(user, field):
            setattr(user, field, value)
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user

# ============ MEMORY ROUTES ============
@app.post("/api/memories/", response_model=MemoryResponse, tags=["Memories"])
async def create_memory(user_id: int, memory: MemoryCreate, db: Session = Depends(get_db)):
    """Create a new memory"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_memory = Memory(
        user_id=user_id,
        type=memory.type,
        title=memory.title,
        body=memory.body,
        tag=memory.tag,
        accent=memory.accent
    )
    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)
    return new_memory

@app.get("/api/memories/{user_id}", response_model=list, tags=["Memories"])
async def get_user_memories(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all memories for a user"""
    memories = db.query(Memory).filter(Memory.user_id == user_id).offset(skip).limit(limit).all()
    return memories

@app.get("/api/memories/{user_id}/{memory_id}", response_model=MemoryResponse, tags=["Memories"])
async def get_memory(user_id: int, memory_id: int, db: Session = Depends(get_db)):
    """Get a specific memory"""
    memory = db.query(Memory).filter(Memory.user_id == user_id, Memory.id == memory_id).first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory

@app.put("/api/memories/{user_id}/{memory_id}", response_model=MemoryResponse, tags=["Memories"])
async def update_memory(user_id: int, memory_id: int, memory_data: MemoryCreate, db: Session = Depends(get_db)):
    """Update a memory"""
    memory = db.query(Memory).filter(Memory.user_id == user_id, Memory.id == memory_id).first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    
    memory.type = memory_data.type
    memory.title = memory_data.title
    memory.body = memory_data.body
    memory.tag = memory_data.tag
    memory.accent = memory_data.accent
    memory.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(memory)
    return memory

@app.delete("/api/memories/{user_id}/{memory_id}", tags=["Memories"])
async def delete_memory(user_id: int, memory_id: int, db: Session = Depends(get_db)):
    """Delete a memory"""
    memory = db.query(Memory).filter(Memory.user_id == user_id, Memory.id == memory_id).first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    
    db.delete(memory)
    db.commit()
    return {"message": "Memory deleted successfully"}

# ============ CHAT ROUTES ============
@app.post("/api/chat/{user_id}", response_model=ChatMessageResponse, tags=["Chat"])
async def save_chat_message(user_id: int, message: ChatMessageCreate, db: Session = Depends(get_db)):
    """Save a chat message"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_message = ChatMessage(
        user_id=user_id,
        role=message.role,
        model=message.model,
        text=message.text
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@app.get("/api/chat/{user_id}", response_model=list, tags=["Chat"])
async def get_chat_history(user_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """Get chat history for a user"""
    messages = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    return messages[::-1]

# ============ KNOWLEDGE GRAPH ROUTES ============
@app.post("/api/knowledge/nodes/{user_id}", response_model=KnowledgeNodeResponse, tags=["Knowledge Graph"])
async def create_node(user_id: int, node: KnowledgeNodeCreate, db: Session = Depends(get_db)):
    """Create a knowledge graph node"""
    new_node = KnowledgeNode(
        user_id=user_id,
        label=node.label,
        type=node.type,
        color=node.color,
        x=node.x,
        y=node.y,
        r=node.r
    )
    db.add(new_node)
    db.commit()
    db.refresh(new_node)
    return new_node

@app.get("/api/knowledge/nodes/{user_id}", response_model=list, tags=["Knowledge Graph"])
async def get_user_nodes(user_id: int, db: Session = Depends(get_db)):
    """Get all knowledge nodes for a user"""
    nodes = db.query(KnowledgeNode).filter(KnowledgeNode.user_id == user_id).all()
    return nodes

@app.delete("/api/knowledge/nodes/{user_id}/{node_id}", tags=["Knowledge Graph"])
async def delete_node(user_id: int, node_id: int, db: Session = Depends(get_db)):
    """Delete a knowledge node"""
    node = db.query(KnowledgeNode).filter(KnowledgeNode.user_id == user_id, KnowledgeNode.id == node_id).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    db.delete(node)
    db.commit()
    return {"message": "Node deleted successfully"}

# ============ ACTIVITY LOG ROUTES ============
@app.post("/api/activity/{user_id}", response_model=ActivityLogResponse, tags=["Activity"])
async def log_activity(user_id: int, activity_data: dict, db: Session = Depends(get_db)):
    """Log a user activity"""
    new_activity = ActivityLog(
        user_id=user_id,
        action=activity_data.get("action"),
        object_type=activity_data.get("object_type"),
        object_name=activity_data.get("object_name"),
        status=activity_data.get("status", "completed")
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

@app.get("/api/activity/{user_id}", response_model=list, tags=["Activity"])
async def get_user_activity(user_id: int, limit: int = 20, db: Session = Depends(get_db)):
    """Get activity timeline for a user"""
    activities = db.query(ActivityLog).filter(ActivityLog.user_id == user_id).order_by(ActivityLog.created_at.desc()).limit(limit).all()
    return activities[::-1]

# ============ MODEL ROUTER ROUTES ============
@app.post("/api/router/{user_id}", tags=["AI Router"])
async def create_router_rule(user_id: int, router_data: dict, db: Session = Depends(get_db)):
    """Create a model routing rule"""
    new_rule = ModelRouter(
        user_id=user_id,
        task=router_data.get("task"),
        model=router_data.get("model"),
        reason=router_data.get("reason"),
        active=router_data.get("active", True)
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return {"id": new_rule.id, "message": "Routing rule created"}

@app.get("/api/router/{user_id}", tags=["AI Router"])
async def get_router_rules(user_id: int, db: Session = Depends(get_db)):
    """Get all routing rules for a user"""
    rules = db.query(ModelRouter).filter(ModelRouter.user_id == user_id).all()
    return rules

# ============ NOTIFICATIONS ROUTES ============
@app.post("/api/notifications/{user_id}", response_model=NotificationResponse, tags=["Notifications"])
async def create_notification(user_id: int, notif_data: dict, db: Session = Depends(get_db)):
    """Create a notification"""
    new_notif = Notification(
        user_id=user_id,
        type=notif_data.get("type"),
        message=notif_data.get("message"),
        icon=notif_data.get("icon")
    )
    db.add(new_notif)
    db.commit()
    db.refresh(new_notif)
    return new_notif

@app.get("/api/notifications/{user_id}", response_model=list, tags=["Notifications"])
async def get_user_notifications(user_id: int, unread_only: bool = False, db: Session = Depends(get_db)):
    """Get notifications for a user"""
    query = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        query = query.filter(Notification.read == False)
    notifications = query.order_by(Notification.created_at.desc()).all()
    return notifications

@app.put("/api/notifications/{user_id}/{notif_id}/read", tags=["Notifications"])
async def mark_as_read(user_id: int, notif_id: int, db: Session = Depends(get_db)):
    """Mark notification as read"""
    notif = db.query(Notification).filter(Notification.user_id == user_id, Notification.id == notif_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notif.read = True
    db.commit()
    return {"message": "Notification marked as read"}

# ============ STATS ROUTES ============
@app.get("/api/stats/{user_id}", tags=["Stats"])
async def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """Get user statistics"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    memories_count = db.query(Memory).filter(Memory.user_id == user_id).count()
    nodes_count = db.query(KnowledgeNode).filter(KnowledgeNode.user_id == user_id).count()
    messages_count = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).count()
    
    return {
        "user_id": user_id,
        "memories_stored": memories_count,
        "sessions_synced": user.total_sessions,
        "knowledge_nodes": nodes_count,
        "chat_messages": messages_count,
        "hours_saved": 38,
        "accuracy_rate": 94.2,
        "response_time": 340,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
