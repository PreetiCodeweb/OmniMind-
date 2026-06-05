const { useState } = React;

const App = () => {
  const [active, setActive] = useState('dashboard');
  const titles = {
  dashboard: 'Dashboard',
  chat: 'Chat',
  passport: 'AI Passport',
  vault: 'Memory Vault',
  graph: 'Knowledge Graph',
  router: 'AI Router',
  games: 'OmniMind Arcade',
  settings: 'Settings',
};
  const renderView = () => {
    switch (active) {
      case 'dashboard': return <Dashboard setActive={setActive} />;
      case 'chat': return <ChatView />;
      case 'passport': return <PassportView />;
      case 'vault': return <VaultView />;
      case 'graph': return <GraphView />;
      case 'router': return <RouterView />;
      case 'games': return <GamesView />;
      case 'settings': return <SettingsView />;
      default: return <Dashboard setActive={setActive} />;
    }
  };

  return (
    <>
      <Notifications />
      <div className="app">
        <Sidebar active={active} setActive={setActive} />
        <div className="main">
          <div className="topbar">
            <span className="topbar-title">{titles[active]}</span>
            <div className="topbar-sep"></div>
            <div className="model-selector">
              <div className="model-selector-dot"></div>
              Auto-routing active
              <span style={{ fontSize: '10px', color: 'var(--text-muted)', marginLeft: '2px' }}>▾</span>
            </div>
            <div className="topbar-actions">
              <button className="icon-btn" title="Search">⊙</button>
              <button className="icon-btn" title="Notifications">◉</button>
              <button className="icon-btn" title="Memory Sync">◈</button>
            </div>
          </div>
          {renderView()}
        </div>
      </div>
    </>
  );
};
