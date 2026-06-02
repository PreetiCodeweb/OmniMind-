const { useState, useEffect } = React;

const Dashboard = ({ setActive }) => {
  const [animated, setAnimated] = useState(false);

  useEffect(() => {
    const timeout = setTimeout(() => setAnimated(true), 100);
    return () => clearTimeout(timeout);
  }, []);

  const kgData = [
    { label: 'AI Engineering', color: '#4d9cff', pct: 88 },
    { label: 'Mathematics', color: '#a78bfa', pct: 72 },
    { label: 'Startup Building', color: '#34d399', pct: 65 },
    { label: 'Trading & Finance', color: '#fbbf24', pct: 54 },
    { label: 'Research Methods', color: '#22d3ee', pct: 47 },
  ];

  const recentActivity = [
    { color: '#34d399', bg: 'rgba(52,211,153,0.15)', initial: 'C', text: <>Claude extracted <strong>3 new memories</strong> from your architecture discussion</>, time: '9 min ago' },
    { color: '#4d9cff', bg: 'rgba(77,156,255,0.15)', initial: 'G', text: <>Gemini completed <strong>API documentation</strong> for the RAG pipeline</>, time: '2h ago' },
    { color: '#a78bfa', bg: 'rgba(167,139,250,0.15)', initial: 'M', text: <>Memory Vault updated with <strong>12 new nodes</strong> in your Knowledge Graph</>, time: 'Yesterday' },
    { color: '#fbbf24', bg: 'rgba(251,191,36,0.15)', initial: 'G', text: <>Grok answered real-time market data request using your investor context</>, time: '2d ago' },
  ];

  return (
    <div className="content">
      <div className="greeting">
        <h1>Good morning, {USER_PROFILE.name} ✦</h1>
        <p>Your AI memory is active across {MODELS.length} connected models · 3 pending memory suggestions</p>
      </div>

      <div className="stats-grid">
        {[
          { label: 'Memories Stored', value: QUICK_STATS.memoriesStored.toLocaleString(), sub: '+12 this week', cls: 'stat-accent-blue' },
          { label: 'Sessions Synced', value: QUICK_STATS.sessionsSynced, sub: `Across ${MODELS.length} models`, cls: 'stat-accent-purple' },
          { label: 'Knowledge Nodes', value: (QUICK_STATS.knowledgeNodes / 1000).toFixed(1) + 'k', sub: 'Growing graph', cls: 'stat-accent-green' },
          { label: 'Hours Saved', value: QUICK_STATS.hoursSaved, sub: 'Vs. re-explaining', cls: 'stat-accent-amber' },
        ].map((s, i) => (
          <div key={i} className={`stat-card ${s.cls}`}>
            <div className="stat-label">{s.label}</div>
            <div className="stat-value">{s.value}</div>
            <div className="stat-sub">{s.sub}</div>
          </div>
        ))}
      </div>

      <div className="section-grid">
        <div className="panel">
          <div className="panel-title">Knowledge Growth <span>Last 30 days</span></div>
          <div className="kg-nodes">
            {kgData.map((k, i) => (
              <div key={i} className="kg-node">
                <div className="kg-dot" style={{ background: k.color }}></div>
                <div className="kg-label">{k.label}</div>
                <div className="kg-bar" style={{ maxWidth: '140px' }}>
                  <div className="kg-fill" style={{ width: animated ? `${k.pct}%` : '0%', background: k.color }}></div>
                </div>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)', width: '28px', textAlign: 'right' }}>{k.pct}%</div>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-title">Recent Activity</div>
          <div className="activity-list">
            {recentActivity.map((a, i) => (
              <div key={i} className="activity-item">
                <div className="activity-avatar" style={{ background: a.bg, color: a.color, fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: '11px' }}>{a.initial}</div>
                <div className="activity-body">
                  <div className="activity-text">{a.text}</div>
                  <div className="activity-time">{a.time}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="section-grid">
        <div className="panel">
          <div className="panel-title">AI Router — Active Routing <span>Auto mode</span></div>
          <div className="router-grid">
            {[
              { task: 'Coding', model: 'Claude', badge: 'badge-green', bdg: 'Optimal' },
              { task: 'Research', model: 'Gemini', badge: 'badge-blue', bdg: 'Active' },
              { task: 'Reasoning', model: 'GPT-4o', badge: 'badge-purple', bdg: 'Ready' },
              { task: 'Real-time', model: 'Grok 3', badge: 'badge-amber', bdg: 'Live' },
              { task: 'Images', model: 'GPT Vision', badge: 'badge-cyan', bdg: 'Ready' },
              { task: 'Docs', model: 'Gemini', badge: 'badge-blue', bdg: 'Active' },
            ].map((r, i) => (
              <div key={i} className={`router-item ${i < 2 ? 'active' : ''}`}>
                <div className="router-task">{r.task}</div>
                <div className="router-model">{r.model}</div>
                <span className={`router-badge ${r.badge}`}>{r.bdg}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-title">Recent Memories</div>
          <div className="memory-list">
            {MEMORY_DATA.slice(0, 3).map(m => (
              <div key={m.id} className="memory-item" onClick={() => {}}>
                <div style={{ fontSize: '14px', color: m.accent, marginTop: '1px' }}>◈</div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div className="memory-title">{m.title}</div>
                  <div className="memory-meta">{m.type} · {m.date} <span className={`memory-tag ${m.tagColor}`} style={{ background: 'rgba(77,156,255,0.1)', color: m.accent, padding: '1px 6px', borderRadius: '99px', fontSize: '10px' }}>{m.tag}</span></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
