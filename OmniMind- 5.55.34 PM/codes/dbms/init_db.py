#!/usr/bin/env python3
"""
Database Initialization Script
Populates the OmniMind database with seed data
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy.orm import Session
from app import engine, SessionLocal, Base, User, Memory, ChatMessage, KnowledgeNode, KnowledgeEdge, ActivityLog, ModelRouter, Notification

def init_database():
    """Create all database tables"""
    print("🔄 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

def seed_users(db: Session):
    """Insert sample users"""
    users = [
        {
            "name": "Preeti Sasmal",
            "email": "preeti@omnimind.io",
            "tier": "Pro",
            "avatar": "P",
            "total_sessions": 24,
            "streak": 7
        },
        {
            "name": "Alice Chen",
            "email": "alice@omnimind.io",
            "tier": "Free",
            "avatar": "A",
            "total_sessions": 5,
            "streak": 2
        },
        {
            "name": "Bob Johnson",
            "email": "bob@omnimind.io",
            "tier": "Pro",
            "avatar": "B",
            "total_sessions": 18,
            "streak": 5
        },
        {
            "name": "Sarah Williams",
            "email": "sarah@omnimind.io",
            "tier": "Enterprise",
            "avatar": "S",
            "total_sessions": 42,
            "streak": 12
        }
    ]
    
    for user_data in users:
        user = User(**user_data)
        db.add(user)
    
    db.commit()
    print("✅ Seeded 4 users")
    return db.query(User).all()

def seed_memories(db: Session, users):
    """Insert sample memories"""
    memories_data = [
        # Preeti's memories
        (users[0].id, "Goal", "Build OmniMind SaaS", "Create AI-powered memory management platform with React frontend and FastAPI backend", "Career", "#4d9cff"),
        (users[0].id, "Project", "Complete Backend API", "Implement all CRUD endpoints and database models for OmniMind", "Career", "#7c3aed"),
        (users[0].id, "Skill", "Master FastAPI", "Learn FastAPI framework for building scalable async web APIs", "Learning", "#06b6d4"),
        (users[0].id, "Decision", "Use PostgreSQL for Production", "Decision to migrate from SQLite to PostgreSQL for production deployment", "Technical", "#f59e0b"),
        (users[0].id, "Research", "AI Memory Techniques", "Study vector embeddings and semantic search for memory retrieval", "Research", "#8b5cf6"),
        (users[0].id, "Preference", "Daily Standup at 9 AM", "Personal preference: start work day with team standup meeting", "Personal", "#ec4899"),
        
        # Alice's memories
        (users[1].id, "Goal", "Learn React Hooks", "Master React Hooks for functional components and state management", "Learning", "#4d9cff"),
        (users[1].id, "Project", "Build Portfolio Website", "Create personal portfolio showcasing projects and skills", "Career", "#7c3aed"),
        (users[1].id, "Skill", "TypeScript Basics", "Understand TypeScript fundamentals and type system", "Learning", "#06b6d4"),
        
        # Bob's memories
        (users[2].id, "Goal", "Become a Full-Stack Developer", "Develop expertise in both frontend and backend development", "Career", "#4d9cff"),
        (users[2].id, "Project", "Deploy First App", "Deploy a full-stack application to production", "Career", "#7c3aed"),
        (users[2].id, "Decision", "Docker for Containerization", "Use Docker for application deployment and scaling", "Technical", "#f59e0b"),
        
        # Sarah's memories
        (users[3].id, "Goal", "Build AI Product", "Create AI-powered SaaS product for enterprise market", "Career", "#4d9cff"),
        (users[3].id, "Project", "Vector Database Integration", "Integrate pgvector for semantic search capabilities", "Technical", "#7c3aed"),
        (users[3].id, "Research", "LLM Fine-tuning", "Research techniques for fine-tuning large language models", "Research", "#8b5cf6"),
    ]
    
    for user_id, mem_type, title, body, tag, accent in memories_data:
        memory = Memory(user_id=user_id, type=mem_type, title=title, body=body, tag=tag, accent=accent)
        db.add(memory)
    
    db.commit()
    print(f"✅ Seeded {len(memories_data)} memories")

def seed_chat_messages(db: Session, users):
    """Insert sample chat messages"""
    messages_data = [
        # Preeti's chats
        (users[0].id, "user", "Claude", "How do I structure a FastAPI project for scalability?"),
        (users[0].id, "ai", "Claude", "For FastAPI scalability, organize code into modular routes, use dependency injection, implement proper logging, and leverage async operations. Consider using SQLAlchemy ORM for database abstraction."),
        (users[0].id, "user", "Claude", "What are best practices for API documentation?"),
        (users[0].id, "ai", "Claude", "Use OpenAPI/Swagger specs, document all endpoints with examples, include error codes, provide authentication details, and maintain updated API changelog."),
        
        # Alice's chats
        (users[1].id, "user", "GPT-4o", "Explain React Hooks in simple terms"),
        (users[1].id, "ai", "GPT-4o", "React Hooks are functions that let you use state and other React features in functional components. Common ones: useState (state), useEffect (side effects), useContext (context)."),
        
        # Bob's chats
        (users[2].id, "user", "Gemini", "Best Docker practices for web apps?"),
        (users[2].id, "ai", "Gemini", "Use multi-stage builds, minimize image size, never run as root, use specific base image versions, implement health checks, and manage secrets with environment files."),
        
        # Sarah's chats
        (users[3].id, "user", "Claude", "How do vector databases improve search?"),
        (users[3].id, "ai", "Claude", "Vector databases store embeddings of data and enable semantic search. They find similar items based on meaning, not just keywords, using distance metrics like cosine similarity."),
    ]
    
    for user_id, role, model, text in messages_data:
        message = ChatMessage(user_id=user_id, role=role, model=model, text=text)
        db.add(message)
    
    db.commit()
    print(f"✅ Seeded {len(messages_data)} chat messages")

def seed_knowledge_nodes(db: Session, users):
    """Insert sample knowledge nodes"""
    nodes_data = [
        # Preeti's knowledge graph
        (users[0].id, "OmniMind", "root", "#4d9cff", 0, 0, 60),
        (users[0].id, "Backend", "main", "#7c3aed", -150, -100, 45),
        (users[0].id, "Frontend", "main", "#06b6d4", 150, -100, 45),
        (users[0].id, "Database", "main", "#f59e0b", 0, 150, 45),
        (users[0].id, "FastAPI", "sub", "#7c3aed", -200, -180, 30),
        (users[0].id, "SQLAlchemy", "sub", "#f59e0b", -50, 200, 30),
        (users[0].id, "React", "sub", "#06b6d4", 200, -180, 30),
        (users[0].id, "PostgreSQL", "sub", "#f59e0b", 50, 220, 30),
        
        # Alice's knowledge graph
        (users[1].id, "React Learning", "root", "#4d9cff", 0, 0, 50),
        (users[1].id, "Hooks", "main", "#06b6d4", 100, 100, 35),
        (users[1].id, "State Management", "main", "#7c3aed", -100, 100, 35),
        
        # Bob's knowledge graph
        (users[2].id, "Full Stack Dev", "root", "#4d9cff", 0, 0, 50),
        (users[2].id, "Frontend Skills", "main", "#06b6d4", -120, -80, 35),
        (users[2].id, "Backend Skills", "main", "#7c3aed", 120, -80, 35),
        
        # Sarah's knowledge graph
        (users[3].id, "AI Product", "root", "#4d9cff", 0, 0, 60),
        (users[3].id, "ML/AI", "main", "#8b5cf6", -150, 100, 40),
        (users[3].id, "Vector Search", "main", "#f59e0b", 150, 100, 40),
    ]
    
    for user_id, label, node_type, color, x, y, r in nodes_data:
        node = KnowledgeNode(user_id=user_id, label=label, type=node_type, color=color, x=x, y=y, r=r)
        db.add(node)
    
    db.commit()
    print(f"✅ Seeded {len(nodes_data)} knowledge nodes")

def seed_activity_logs(db: Session, users):
    """Insert sample activity logs"""
    activities_data = [
        # Preeti's activities
        (users[0].id, "Created", "Memory", "Build OmniMind SaaS", "completed"),
        (users[0].id, "Updated", "Memory", "Complete Backend API", "completed"),
        (users[0].id, "Created", "ChatSession", "FastAPI Architecture Discussion", "completed"),
        (users[0].id, "Created", "KnowledgeNode", "OmniMind Root", "completed"),
        (users[0].id, "Created", "KnowledgeNode", "Backend Module", "completed"),
        
        # Alice's activities
        (users[1].id, "Created", "Memory", "Learn React Hooks", "completed"),
        (users[1].id, "Started", "Course", "React Fundamentals", "pending"),
        
        # Bob's activities
        (users[2].id, "Created", "Project", "Full Stack App", "in_progress"),
        (users[2].id, "Updated", "Memory", "Become Full-Stack Dev", "completed"),
        
        # Sarah's activities
        (users[3].id, "Created", "Research", "Vector DB Study", "completed"),
        (users[3].id, "Created", "Project", "AI Product MVP", "in_progress"),
    ]
    
    for user_id, action, obj_type, obj_name, status in activities_data:
        activity = ActivityLog(user_id=user_id, action=action, object_type=obj_type, object_name=obj_name, status=status)
        db.add(activity)
    
    db.commit()
    print(f"✅ Seeded {len(activities_data)} activity logs")

def seed_model_routers(db: Session, users):
    """Insert sample model routing rules"""
    routers_data = [
        # Preeti's routing rules
        (users[0].id, "Code Review", "Claude", "Best for detailed code analysis and architectural decisions", True),
        (users[0].id, "Documentation", "GPT-4o", "Excellent at clear, structured documentation", True),
        (users[0].id, "Research", "Gemini", "Great for comprehensive research summaries", True),
        
        # Alice's routing rules
        (users[1].id, "Learning", "Claude", "Better explanations for learning new concepts", True),
        (users[1].id, "Quick Answers", "GPT-4o", "Faster responses for quick questions", True),
        
        # Bob's routing rules
        (users[2].id, "Technical Problems", "Claude", "Superior problem-solving for complex technical issues", True),
        (users[2].id, "General Questions", "Gemini", "Good balance of speed and quality", True),
        
        # Sarah's routing rules
        (users[3].id, "AI/ML Topics", "Claude", "Most knowledgeable about AI/ML topics", True),
        (users[3].id, "Product Strategy", "GPT-4o", "Great for product thinking and strategy", True),
        (users[3].id, "Market Research", "Gemini", "Good for market research and analysis", True),
    ]
    
    for user_id, task, model, reason, active in routers_data:
        router = ModelRouter(user_id=user_id, task=task, model=model, reason=reason, active=active)
        db.add(router)
    
    db.commit()
    print(f"✅ Seeded {len(routers_data)} model routing rules")

def seed_notifications(db: Session, users):
    """Insert sample notifications"""
    notifs_data = [
        # Preeti's notifications
        (users[0].id, "success", "Memory saved successfully", "✓", True),
        (users[0].id, "info", "New AI model available: GPT-4o", "ℹ", False),
        (users[0].id, "warning", "Approaching storage limit", "⚠", False),
        
        # Alice's notifications
        (users[1].id, "success", "Course enrollment completed", "✓", True),
        (users[1].id, "info", "New learning resource available", "ℹ", False),
        
        # Bob's notifications
        (users[2].id, "success", "Project created", "✓", True),
        (users[2].id, "info", "You have 5 teammates added", "ℹ", True),
        
        # Sarah's notifications
        (users[3].id, "warning", "API rate limit reached", "⚠", False),
        (users[3].id, "success", "Vector database synced", "✓", True),
        (users[3].id, "info", "New beta features available", "ℹ", False),
    ]
    
    for user_id, notif_type, message, icon, read in notifs_data:
        notif = Notification(user_id=user_id, type=notif_type, message=message, icon=icon, read=read)
        db.add(notif)
    
    db.commit()
    print(f"✅ Seeded {len(notifs_data)} notifications")

def main():
    """Main seeding function"""
    print("🚀 OmniMind Database Initialization\n")
    
    try:
        # Initialize database
        init_database()
        
        # Create session
        db = SessionLocal()
        
        # Seed all data
        print("\n📊 Seeding data...\n")
        users = seed_users(db)
        seed_memories(db, users)
        seed_chat_messages(db, users)
        seed_knowledge_nodes(db, users)
        seed_activity_logs(db, users)
        seed_model_routers(db, users)
        seed_notifications(db, users)
        
        db.close()
        
        print("\n✅ Database initialization complete!")
        print("📈 Summary:")
        print("   • 4 users")
        print("   • 15 memories")
        print("   • 10 chat messages")
        print("   • 17 knowledge nodes")
        print("   • 11 activity logs")
        print("   • 10 model routing rules")
        print("   • 10 notifications")
        print("\n🎉 OmniMind database is ready to use!")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
