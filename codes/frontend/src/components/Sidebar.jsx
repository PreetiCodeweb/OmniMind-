const Sidebar = ({ active, setActive }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-mark">U</div>
        <div>
          <div className="logo-text">OmniMind</div>
          <div className="logo-sub">Memory Layer</div>
        </div>
      </div>

      <div className="sidebar-section">
        <div className="sidebar-label">Workspace</div>
        {MENU_ITEMS.slice(0, 6).map(item => (
          <div key={item.id} className={`nav-item ${active === item.id ? 'active' : ''}`} onClick={() => setActive(item.id)}>
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
            {item.badge && <span className={`nav-badge ${item.badge.color === 'green' ? 'green' : ''}`}>{item.badge.count}</span>}
          </div>
        ))}
      </div>

      <div className="sidebar-section" style={{ marginTop: '8px' }}>
        <div className="sidebar-label">Connected Models</div>
        <div className="sidebar-models">
          {MODELS.slice(0, 4).map(m => (
            <div key={m.id} className="model-chip connected">
              <div className="model-dot" style={{ background: m.dot }}></div>
              <span style={{ fontSize: '12.5px' }}>{m.name}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="sidebar-footer">
        <div className="nav-item" style={{ marginBottom: '6px' }} onClick={() => setActive('settings')}>
          <span className="nav-icon">◎</span>
          <span>Settings</span>
        </div>
        <div className="user-row">
          <div className="user-avatar">{USER_PROFILE.avatar}</div>
          <div>
            <div className="user-name">{USER_PROFILE.name}</div>
            <div className="user-plan">{USER_PROFILE.tier} · {USER_PROFILE.email.split('@')[0]}</div>
          </div>
        </div>
      </div>
    </div>
  );
};
