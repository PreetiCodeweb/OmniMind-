const PassportView = () => {
  const skills = [
    { label: 'Python / FastAPI', pct: 88, color: '#4d9cff' },
    { label: 'Machine Learning', pct: 75, color: '#a78bfa' },
    { label: 'System Design', pct: 70, color: '#34d399' },
    { label: 'Mathematics', pct: 82, color: '#fbbf24' },
    { label: 'Product Strategy', pct: 65, color: '#22d3ee' },
  ];

  return (
    <div className="content">
      <div className="content-header">
        <h2>AI Passport</h2>
        <button className="action-btn secondary">✎ Edit Profile</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        <div>
          <div className="passport-card">
            <div className="passport-bg"></div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '14px' }}>
              <div style={{ width: '52px', height: '52px', borderRadius: '50%', background: 'linear-gradient(135deg,#4d9cff,#a78bfa)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'var(--font-heading)', fontWeight: 800, fontSize: '20px', color: '#fff' }}>P</div>
              <div>
                <div className="passport-name">Preeti</div>
                <div className="passport-role">AI Entrepreneur · Engineer</div>
              </div>
            </div>
            <div className="passport-tags">
              {['Artificial Intelligence', 'Mathematics', 'Trading', 'Startup Building', 'Research', 'ML Engineering'].map(t => (
                <span key={t} className="ptag">{t}</span>
              ))}
            </div>
            <div className="passport-stat-row">
              <div className="passport-stat"><div className="passport-stat-n">847</div><div className="passport-stat-l">Memories</div></div>
              <div className="passport-stat"><div className="passport-stat-n">124</div><div className="passport-stat-l">Sessions</div></div>
              <div className="passport-stat"><div className="passport-stat-n">4</div><div className="passport-stat-l">Models</div></div>
            </div>
          </div>

          <div className="panel">
            <div className="panel-title">Active Projects</div>
            {[
              { name: 'UAMIL Platform', status: 'Active', color: '#34d399' },
              { name: 'Medical Dashboard', status: 'Paused', color: '#fbbf24' },
              { name: 'AI Research Assistant', status: 'Planning', color: '#4d9cff' },
            ].map((p, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', padding: '10px 0', borderBottom: i < 2 ? '1px solid var(--border-subtle)' : 'none' }}>
                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: p.color, marginRight: '10px', flexShrink: 0 }}></div>
                <span style={{ fontSize: '13.5px', color: 'var(--text-primary)', flex: 1 }}>{p.name}</span>
                <span style={{ fontSize: '11px', padding: '2px 8px', borderRadius: '99px', background: `${p.color}18`, color: p.color }}>{p.status}</span>
              </div>
            ))}
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div className="panel">
            <div className="panel-title">Skill Map</div>
            {skills.map((s, i) => (
              <div key={i} style={{ marginBottom: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                  <span style={{ fontSize: '12.5px', color: 'var(--text-secondary)' }}>{s.label}</span>
                  <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{s.pct}%</span>
                </div>
                <div className="progress"><div className="progress-fill" style={{ width: `${s.pct}%`, background: s.color }}></div></div>
              </div>
            ))}
          </div>

          <div className="panel">
            <div className="panel-title">Learning Style</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {['Detailed step-by-step explanations', 'Code examples with every concept', 'Visual diagrams and architecture charts', 'Iterative refinement over big-bang solutions', 'Prefer concise summaries after deep dives'].map((l, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: 'var(--text-secondary)' }}>
                  <span style={{ color: 'var(--accent-blue)', fontSize: '10px' }}>◆</span>{l}
                </div>
              ))}
            </div>
          </div>

          <div className="panel">
            <div className="panel-title">Long-term Goals</div>
            {['Build and launch UAMIL as a funded SaaS', 'Become a recognized AI infrastructure engineer', 'Publish research on personal knowledge graphs'].map((g, i) => (
              <div key={i} style={{ display: 'flex', gap: '10px', padding: '8px 0', borderBottom: i < 2 ? '1px solid var(--border-subtle)' : 'none', fontSize: '13px', color: 'var(--text-secondary)' }}>
                <span style={{ color: 'var(--accent-purple)' }}>◉</span>{g}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
