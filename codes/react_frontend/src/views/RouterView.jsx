const RouterView = () => {
  const routerData = [
    { task: 'Code Generation', model: 'Claude Sonnet 4', reason: 'Best at code accuracy + your style prefs', color: '#34d399', active: true },
    { task: 'Architecture Review', model: 'Claude Sonnet 4', reason: 'Knows your UAMIL codebase context', color: '#34d399', active: true },
    { task: 'Research & Analysis', model: 'Gemini Pro', reason: 'Long context + real-time web access', color: '#4d9cff', active: true },
    { task: 'Mathematical Reasoning', model: 'GPT-4o', reason: 'Strong chain-of-thought for proofs', color: '#a78bfa', active: true },
    { task: 'Real-time Information', model: 'Grok 3', reason: 'Latest data, crypto & market trends', color: '#fbbf24', active: false },
    { task: 'Image Generation', model: 'GPT Vision', reason: 'DALL-E 3 for technical diagrams', color: '#22d3ee', active: false },
    { task: 'Documentation', model: 'Gemini Pro', reason: 'Long-form writing + structured output', color: '#4d9cff', active: true },
    { task: 'Translation & Localization', model: 'Mistral Large', reason: 'Multilingual fluency', color: '#f87171', active: false },
  ];

  return (
    <div className="content">
      <div className="content-header">
        <h2>AI Router</h2>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Auto-routing</span>
          <label className="toggle"><input type="checkbox" defaultChecked /><span className="toggle-slider"></span></label>
          <button className="action-btn primary" style={{ marginLeft: '8px' }}>+ Add Rule</button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
        {MODELS.map(m => (
          <div key={m.id} className="panel" style={{ display: 'flex', alignItems: 'center', gap: '14px', padding: '14px 18px' }}>
            <div style={{ width: '40px', height: '40px', borderRadius: 'var(--radius-md)', background: `${m.dot}18`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px', fontFamily: 'var(--font-heading)', fontWeight: 700, color: m.dot, flexShrink: 0 }}>{m.name[0]}</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '13.5px', fontWeight: 500, color: 'var(--text-primary)' }}>{m.name}</div>
              <div style={{ fontSize: '11.5px', color: 'var(--text-muted)', marginTop: '2px' }}>{m.task}</div>
            </div>
            <div style={{ fontSize: '11px', padding: '3px 9px', borderRadius: '99px', background: `${m.dot}18`, color: m.dot }}>Connected</div>
          </div>
        ))}
      </div>

      <div className="panel">
        <div className="panel-title">Routing Rules</div>
        <table className="router-table">
          <thead>
            <tr><th>Task Type</th><th>Routed To</th><th>Reason</th><th>Status</th></tr>
          </thead>
          <tbody>
            {routerData.map((r, i) => (
              <tr key={i}>
                <td style={{ color: 'var(--text-primary)', fontWeight: 500 }}>{r.task}</td>
                <td><span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><div style={{ width: '6px', height: '6px', borderRadius: '50%', background: r.color, flexShrink: 0 }}></div>{r.model}</span></td>
                <td style={{ fontSize: '12px' }}>{r.reason}</td>
                <td><span style={{ fontSize: '11px', padding: '2px 8px', borderRadius: '99px', background: r.active ? 'rgba(52,211,153,0.12)' : 'rgba(75,82,100,0.3)', color: r.active ? '#34d399' : 'var(--text-muted)' }}>{r.active ? 'Active' : 'Inactive'}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
