const { useState } = React;

const Notifications = () => {
  const [visible, setVisible] = useState(NOTIFICATIONS.length > 0);
  const [dismissed, setDismissed] = useState([]);

  const visibleNotifications = NOTIFICATIONS.filter(n => !dismissed.includes(n.id));

  const dismiss = (id) => {
    setDismissed(prev => [...prev, id]);
    if (visibleNotifications.length === 1) {
      setVisible(false);
    }
  };

  if (!visible || visibleNotifications.length === 0) return null;

  return (
    <div style={{ position: 'fixed', top: '20px', right: '20px', zIndex: 9000, display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '360px' }}>
      {visibleNotifications.map(notif => (
        <div
          key={notif.id}
          style={{
            background: notif.type === 'success' ? 'rgba(52, 211, 153, 0.12)' : notif.type === 'warning' ? 'rgba(251, 191, 36, 0.12)' : 'rgba(77, 156, 255, 0.12)',
            border: `1px solid ${notif.type === 'success' ? '#34d399' : notif.type === 'warning' ? '#fbbf24' : '#4d9cff'}`,
            borderRadius: 'var(--radius-md)',
            padding: '12px 16px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            fontSize: '13px',
            color: 'var(--text-primary)',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          }}
        >
          <span style={{ fontSize: '16px' }}>{notif.icon}</span>
          <div style={{ flex: 1 }}>
            <div>{notif.message}</div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>{notif.time}</div>
          </div>
          <button
            onClick={() => dismiss(notif.id)}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              fontSize: '16px',
              padding: '4px',
            }}
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
};
