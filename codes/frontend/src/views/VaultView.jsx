const { useState } = React;

const VaultView = () => {
  const [filter, setFilter] = useState('All');
  const filters = ['All', 'Goals', 'Projects', 'Skills', 'Preferences', 'Research', 'Decisions'];
  const filtered = filter === 'All' ? MEMORY_DATA : MEMORY_DATA.filter(m => m.type === filter.slice(0, -1) || m.type === filter);

  return (
    <div className="content">
      <div className="content-header">
        <h2>Memory Vault</h2>
        <div style={{ display: 'flex', gap: '8px' }}>
          <div className="search-bar" style={{ width: '220px' }}>
            <span style={{ fontSize: '14px', color: 'var(--text-muted)' }}>⊙</span>
            <input placeholder="Search memories..." />
          </div>
          <button className="action-btn primary">+ Add Memory</button>
        </div>
      </div>

      <div className="vault-filters">
        {filters.map(f => (
          <button key={f} className={`filter-btn ${filter === f ? 'active' : ''}`} onClick={() => setFilter(f)}>{f}</button>
        ))}
      </div>

      <div className="vault-grid">
        {filtered.map(m => (
          <div key={m.id} className="vault-card">
            <div className="vault-card-accent" style={{ background: `linear-gradient(90deg, ${m.accent}, transparent)` }}></div>
            <div className="vault-card-type">
              <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: m.accent }}></div>
              {m.type}
            </div>
            <div className="vault-card-title">{m.title}</div>
            <div className="vault-card-body">{m.body}</div>
            <div className="vault-card-footer">
              <span className="vault-card-date">{m.date}</span>
              <span className={`memory-tag ${m.tagColor}`} style={{ background: `${m.accent}18`, color: m.accent, padding: '2px 8px', borderRadius: '99px', fontSize: '10px' }}>{m.tag}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
