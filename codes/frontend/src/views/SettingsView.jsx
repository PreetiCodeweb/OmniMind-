const { useState } = React;

const SettingsView = () => {
  const [section, setSection] = useState('passport');
  const sections = [
    { id: 'passport', icon: '◈', label: 'AI Passport' },
    { id: 'memory', icon: '◻', label: 'Memory & Storage' },
    { id: 'models', icon: '⇋', label: 'Model Connections' },
    { id: 'privacy', icon: '◉', label: 'Privacy & Security' },
    { id: 'billing', icon: '◇', label: 'Plan & Billing' },
  ];

  return (
    <div className="content">
      <div className="content-header" style={{ marginBottom: '20px' }}>
        <h2>Settings</h2>
      </div>
      <div className="settings-grid">
        <div className="settings-nav">
          {sections.map(s => (
            <div key={s.id} className={`sn-item ${section === s.id ? 'active' : ''}`} onClick={() => setSection(s.id)}>
              <span>{s.icon}</span>{s.label}
            </div>
          ))}
        </div>
        <div className="settings-body">
          {section === 'passport' && (
            <div className="settings-section">
              {[
                { title: 'Name', desc: 'Preeti', type: 'text' },
                { title: 'Role / Identity', desc: 'AI Entrepreneur · Engineer', type: 'text' },
                { title: 'Communication Style', desc: 'Technical, concise, step-by-step', type: 'text' },
              ].map((r, i) => (
                <div key={i} className="settings-row">
                  <div className="settings-row-label"><div className="settings-row-title">{r.title}</div><div className="settings-row-desc">{r.desc}</div></div>
                  <button className="action-btn secondary" style={{ padding: '5px 12px', fontSize: '12px' }}>Edit</button>
                </div>
              ))}
            </div>
          )}
          {section === 'memory' && (
            <div className="settings-section">
              {[
                { title: 'Auto-capture memories', desc: 'Automatically extract and store memories from conversations', tog: true },
                { title: 'Cross-session learning', desc: 'Allow models to learn from previous conversation patterns', tog: true },
                { title: 'Memory compression', desc: 'Compress older memories to save storage space', tog: false },
                { title: 'Shared memory across models', desc: 'All connected models access the same memory vault', tog: true },
              ].map((r, i) => (
                <div key={i} className="settings-row">
                  <div className="settings-row-label"><div className="settings-row-title">{r.title}</div><div className="settings-row-desc">{r.desc}</div></div>
                  <label className="toggle"><input type="checkbox" defaultChecked={r.tog} /><span className="toggle-slider"></span></label>
                </div>
              ))}
            </div>
          )}
          {section === 'models' && (
            <div className="settings-section">
              {MODELS.map((m, i) => (
                <div key={i} className="settings-row">
                  <div className="settings-row-label">
                    <div className="settings-row-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: m.dot }}></div>{m.name}
                    </div>
                    <div className="settings-row-desc">{m.task}</div>
                  </div>
                  <label className="toggle"><input type="checkbox" defaultChecked={i < 4} /><span className="toggle-slider"></span></label>
                </div>
              ))}
            </div>
          )}
          {section === 'privacy' && (
            <div className="settings-section">
              {[
                { title: 'End-to-end encryption', desc: 'All memories are encrypted at rest and in transit', tog: true },
                { title: 'Provider data access', desc: 'Allow AI providers to use your data for model training', tog: false },
                { title: 'Memory export', desc: 'Enable data portability and export capabilities', tog: true },
                { title: 'Anonymized analytics', desc: 'Share anonymous usage data to improve UAMIL', tog: false },
              ].map((r, i) => (
                <div key={i} className="settings-row">
                  <div className="settings-row-label"><div className="settings-row-title">{r.title}</div><div className="settings-row-desc">{r.desc}</div></div>
                  <label className="toggle"><input type="checkbox" defaultChecked={r.tog} /><span className="toggle-slider"></span></label>
                </div>
              ))}
            </div>
          )}
          {section === 'billing' && (
            <div className="settings-section">
              <div className="settings-row">
                <div className="settings-row-label">
                  <div className="settings-row-title">Current Plan</div>
                  <div className="settings-row-desc">UAMIL Pro — Unlimited memories, 5 models</div>
                </div>
                <span style={{ fontSize: '11px', padding: '3px 10px', borderRadius: '99px', background: 'rgba(77,156,255,0.12)', color: 'var(--accent-blue)', fontWeight: 500 }}>Active</span>
              </div>
              <div className="settings-row">
                <div className="settings-row-label"><div className="settings-row-title">Memory Storage</div><div className="settings-row-desc">847 / 10,000 memories used</div></div>
                <div style={{ width: '120px' }}><div className="progress"><div className="progress-fill" style={{ width: '8.5%', background: 'var(--accent-blue)' }}></div></div></div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
