-- OmniMind Seed Data
-- Sample data for development and testing

-- ============ INSERT SAMPLE USERS ============
INSERT INTO users (name, email, tier, avatar, total_sessions, streak) VALUES
('Preeti Sasmal', 'preeti@omnimind.io', 'Pro', 'P', 24, 7),
('Alice Chen', 'alice@omnimind.io', 'Free', 'A', 5, 2),
('Bob Johnson', 'bob@omnimind.io', 'Pro', 'B', 18, 5),
('Sarah Williams', 'sarah@omnimind.io', 'Enterprise', 'S', 42, 12);

-- ============ INSERT SAMPLE MEMORIES ============
INSERT INTO memories (user_id, type, title, body, tag, accent) VALUES
-- Preeti's memories
(1, 'Goal', 'Build OmniMind SaaS', 'Create AI-powered memory management platform with React frontend and FastAPI backend', 'Career', '#4d9cff'),
(1, 'Project', 'Complete Backend API', 'Implement all CRUD endpoints and database models for OmniMind', 'Career', '#7c3aed'),
(1, 'Skill', 'Master FastAPI', 'Learn FastAPI framework for building scalable async web APIs', 'Learning', '#06b6d4'),
(1, 'Decision', 'Use PostgreSQL for Production', 'Decision to migrate from SQLite to PostgreSQL for production deployment', 'Technical', '#f59e0b'),
(1, 'Research', 'AI Memory Techniques', 'Study vector embeddings and semantic search for memory retrieval', 'Research', '#8b5cf6'),
(1, 'Preference', 'Daily Standup at 9 AM', 'Personal preference: start work day with team standup meeting', 'Personal', '#ec4899'),

-- Alice's memories
(2, 'Goal', 'Learn React Hooks', 'Master React Hooks for functional components and state management', 'Learning', '#4d9cff'),
(2, 'Project', 'Build Portfolio Website', 'Create personal portfolio showcasing projects and skills', 'Career', '#7c3aed'),
(2, 'Skill', 'TypeScript Basics', 'Understand TypeScript fundamentals and type system', 'Learning', '#06b6d4'),

-- Bob's memories
(3, 'Goal', 'Become a Full-Stack Developer', 'Develop expertise in both frontend and backend development', 'Career', '#4d9cff'),
(3, 'Project', 'Deploy First App', 'Deploy a full-stack application to production', 'Career', '#7c3aed'),
(3, 'Decision', 'Docker for Containerization', 'Use Docker for application deployment and scaling', 'Technical', '#f59e0b'),

-- Sarah's memories
(4, 'Goal', 'Build AI Product', 'Create AI-powered SaaS product for enterprise market', 'Career', '#4d9cff'),
(4, 'Project', 'Vector Database Integration', 'Integrate pgvector for semantic search capabilities', 'Technical', '#7c3aed'),
(4, 'Research', 'LLM Fine-tuning', 'Research techniques for fine-tuning large language models', 'Research', '#8b5cf6');

-- ============ INSERT SAMPLE CHAT MESSAGES ============
INSERT INTO chat_messages (user_id, role, model, text) VALUES
-- Preeti's chats
(1, 'user', 'Claude', 'How do I structure a FastAPI project for scalability?'),
(1, 'ai', 'Claude', 'For FastAPI scalability, organize code into modular routes, use dependency injection, implement proper logging, and leverage async operations. Consider using SQLAlchemy ORM for database abstraction.'),
(1, 'user', 'Claude', 'What are best practices for API documentation?'),
(1, 'ai', 'Claude', 'Use OpenAPI/Swagger specs, document all endpoints with examples, include error codes, provide authentication details, and maintain updated API changelog.'),

-- Alice's chats
(2, 'user', 'GPT-4o', 'Explain React Hooks in simple terms'),
(2, 'ai', 'GPT-4o', 'React Hooks are functions that let you use state and other React features in functional components. Common ones: useState (state), useEffect (side effects), useContext (context).'),

-- Bob's chats
(3, 'user', 'Gemini', 'Best Docker practices for web apps?'),
(3, 'ai', 'Gemini', 'Use multi-stage builds, minimize image size, never run as root, use specific base image versions, implement health checks, and manage secrets with environment files.'),

-- Sarah's chats
(4, 'user', 'Claude', 'How do vector databases improve search?'),
(4, 'ai', 'Claude', 'Vector databases store embeddings of data and enable semantic search. They find similar items based on meaning, not just keywords, using distance metrics like cosine similarity.');

-- ============ INSERT SAMPLE KNOWLEDGE NODES ============
INSERT INTO knowledge_nodes (user_id, label, type, color, x, y, r) VALUES
-- Preeti's knowledge graph
(1, 'OmniMind', 'root', '#4d9cff', 0, 0, 60),
(1, 'Backend', 'main', '#7c3aed', -150, -100, 45),
(1, 'Frontend', 'main', '#06b6d4', 150, -100, 45),
(1, 'Database', 'main', '#f59e0b', 0, 150, 45),
(1, 'FastAPI', 'sub', '#7c3aed', -200, -180, 30),
(1, 'SQLAlchemy', 'sub', '#f59e0b', -50, 200, 30),
(1, 'React', 'sub', '#06b6d4', 200, -180, 30),
(1, 'PostgreSQL', 'sub', '#f59e0b', 50, 220, 30),

-- Alice's knowledge graph
(2, 'React Learning', 'root', '#4d9cff', 0, 0, 50),
(2, 'Hooks', 'main', '#06b6d4', 100, 100, 35),
(2, 'State Management', 'main', '#7c3aed', -100, 100, 35),

-- Bob's knowledge graph
(3, 'Full Stack Dev', 'root', '#4d9cff', 0, 0, 50),
(3, 'Frontend Skills', 'main', '#06b6d4', -120, -80, 35),
(3, 'Backend Skills', 'main', '#7c3aed', 120, -80, 35),

-- Sarah's knowledge graph
(4, 'AI Product', 'root', '#4d9cff', 0, 0, 60),
(4, 'ML/AI', 'main', '#8b5cf6', -150, 100, 40),
(4, 'Vector Search', 'main', '#f59e0b', 150, 100, 40);

-- ============ INSERT SAMPLE KNOWLEDGE EDGES ============
INSERT INTO knowledge_edges (user_id, from_node_id, to_node_id) VALUES
-- Preeti's connections
(1, 1, 2), -- OmniMind -> Backend
(1, 1, 3), -- OmniMind -> Frontend
(1, 1, 4), -- OmniMind -> Database
(1, 2, 5), -- Backend -> FastAPI
(1, 4, 6), -- Database -> SQLAlchemy
(1, 3, 7), -- Frontend -> React
(1, 4, 8), -- Database -> PostgreSQL

-- Alice's connections
(2, 1, 2), (2, 1, 3), (2, 2, 3),

-- Bob's connections
(3, 1, 2), (3, 1, 3),

-- Sarah's connections
(4, 1, 2), (4, 1, 3);

-- ============ INSERT SAMPLE ACTIVITY LOGS ============
INSERT INTO activity_logs (user_id, action, object_type, object_name, status) VALUES
-- Preeti's activities
(1, 'Created', 'Memory', 'Build OmniMind SaaS', 'completed'),
(1, 'Updated', 'Memory', 'Complete Backend API', 'completed'),
(1, 'Created', 'ChatSession', 'FastAPI Architecture Discussion', 'completed'),
(1, 'Created', 'KnowledgeNode', 'OmniMind Root', 'completed'),
(1, 'Created', 'KnowledgeNode', 'Backend Module', 'completed'),

-- Alice's activities
(2, 'Created', 'Memory', 'Learn React Hooks', 'completed'),
(2, 'Started', 'Course', 'React Fundamentals', 'pending'),

-- Bob's activities
(3, 'Created', 'Project', 'Full Stack App', 'in_progress'),
(3, 'Updated', 'Memory', 'Become Full-Stack Dev', 'completed'),

-- Sarah's activities
(4, 'Created', 'Research', 'Vector DB Study', 'completed'),
(4, 'Created', 'Project', 'AI Product MVP', 'in_progress');

-- ============ INSERT SAMPLE MODEL ROUTERS ============
INSERT INTO model_routers (user_id, task, model, reason, active) VALUES
-- Preeti's routing rules
(1, 'Code Review', 'Claude', 'Best for detailed code analysis and architectural decisions', 1),
(1, 'Documentation', 'GPT-4o', 'Excellent at clear, structured documentation', 1),
(1, 'Research', 'Gemini', 'Great for comprehensive research summaries', 1),

-- Alice's routing rules
(2, 'Learning', 'Claude', 'Better explanations for learning new concepts', 1),
(2, 'Quick Answers', 'GPT-4o', 'Faster responses for quick questions', 1),

-- Bob's routing rules
(3, 'Technical Problems', 'Claude', 'Superior problem-solving for complex technical issues', 1),
(3, 'General Questions', 'Gemini', 'Good balance of speed and quality', 1),

-- Sarah's routing rules
(4, 'AI/ML Topics', 'Claude', 'Most knowledgeable about AI/ML topics', 1),
(4, 'Product Strategy', 'GPT-4o', 'Great for product thinking and strategy', 1),
(4, 'Market Research', 'Gemini', 'Good for market research and analysis', 1);

-- ============ INSERT SAMPLE NOTIFICATIONS ============
INSERT INTO notifications (user_id, type, message, icon, read) VALUES
-- Preeti's notifications
(1, 'success', 'Memory saved successfully', '✓', 1),
(1, 'info', 'New AI model available: GPT-4o', 'ℹ', 0),
(1, 'warning', 'Approaching storage limit', '⚠', 0),

-- Alice's notifications
(2, 'success', 'Course enrollment completed', '✓', 1),
(2, 'info', 'New learning resource available', 'ℹ', 0),

-- Bob's notifications
(3, 'success', 'Project created', '✓', 1),
(3, 'info', 'You have 5 teammates added', 'ℹ', 1),

-- Sarah's notifications
(4, 'warning', 'API rate limit reached', '⚠', 0),
(4, 'success', 'Vector database synced', '✓', 1),
(4, 'info', 'New beta features available', 'ℹ', 0);
