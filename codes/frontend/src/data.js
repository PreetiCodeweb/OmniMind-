const MODELS = [
  { id: 'claude', name: 'Claude Sonnet', dot: '#34d399', task: 'Code & Architecture' },
  { id: 'gpt', name: 'GPT-4o', dot: '#a78bfa', task: 'Reasoning & Logic' },
  { id: 'gemini', name: 'Gemini Pro', dot: '#4d9cff', task: 'Research & Analysis' },
  { id: 'grok', name: 'Grok 3', dot: '#fbbf24', task: 'Real-time Info' },
  { id: 'mistral', name: 'Mistral Large', dot: '#f87171', task: 'Multilingual' },
];

const MEMORY_DATA = [
  { id: 1, type: 'Goal', title: 'Become an AI Entrepreneur', body: 'Build and ship UAMIL as a SaaS platform by Q3 2025.', date: '2d ago', tag: 'Career', tagColor: 'badge-blue', accent: '#4d9cff' },
  { id: 2, type: 'Project', title: 'UAMIL Frontend Build', body: 'React + FastAPI stack. LobeHub-inspired dark UI with multi-model routing.', date: '1d ago', tag: 'Active', tagColor: 'badge-green', accent: '#34d399' },
  { id: 3, type: 'Skill', title: 'RAG Pipeline Design', body: 'Vector embeddings with FAISS for semantic memory retrieval. Chunking strategy.', date: '3d ago', tag: 'Technical', tagColor: 'badge-purple', accent: '#a78bfa' },
  { id: 4, type: 'Preference', title: 'Learning Style', body: 'Detailed step-by-step explanations with code examples. Prefer visual diagrams.', date: '1w ago', tag: 'Meta', tagColor: 'badge-amber', accent: '#fbbf24' },
  { id: 5, type: 'Research', title: 'AI Memory Architectures', body: 'Surveyed MemGPT, LangMem, Zep. Identified gap in cross-model portability.', date: '5d ago', tag: 'Research', tagColor: 'badge-cyan', accent: '#22d3ee' },
  { id: 6, type: 'Decision', title: 'Tech Stack Choice', body: 'FastAPI for speed, PostgreSQL + pgvector for memory, Redis for session state.', date: '4d ago', tag: 'Architecture', tagColor: 'badge-purple', accent: '#a78bfa' },
];

const CHAT_HISTORY = [
  { id: 1, role: 'ai', model: 'Claude', modelColor: '#34d399', text: 'Good morning! I have your UAMIL project context loaded. You were working on the Knowledge Graph engine — specifically the embedding layer for cross-model memory retrieval. Want to continue?', time: '9:02 AM' },
  { id: 2, role: 'user', text: 'Yes — let\'s design the RAG pipeline for the Memory Vault. I want it to support semantic search across all stored memories.', time: '9:04 AM' },
  { id: 3, role: 'ai', model: 'Claude', modelColor: '#34d399', text: `Here's a clean architecture for your Memory Vault RAG pipeline:\n\n**Ingestion Layer**: Parse conversations → extract entities & intents → chunk into semantic units → embed with text-embedding-3-large.\n\n**Storage Layer**: pgvector for dense retrieval + BM25 for keyword fallback. Store metadata (source model, timestamp, topic tags).\n\n**Retrieval**: Hybrid search with RRF reranking. Filter by recency and relevance score. Top-K with MMR for diversity.\n\nThis gives you fast, accurate recall across your full memory history regardless of which model originally created it.`, time: '9:05 AM' },
  { id: 4, role: 'user', text: 'Perfect. Now route this to Gemini for the research documentation part.', time: '9:08 AM' },
  { id: 5, role: 'ai', model: 'Gemini', modelColor: '#4d9cff', text: 'Switching to Gemini for documentation. I have the architecture from your earlier Claude session in context. I\'ll generate comprehensive API docs and a system design document for the RAG pipeline. Starting with the OpenAPI spec...', time: '9:09 AM' },
];
