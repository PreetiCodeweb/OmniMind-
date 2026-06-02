const { useRef } = React;

const GraphView = () => {
  const svgRef = useRef(null);
  const nodes = [
    { id: 'root', label: 'Preeti', x: 300, y: 180, r: 26, color: '#4d9cff', type: 'root' },
    { id: 'ai', label: 'AI Engineering', x: 160, y: 90, r: 20, color: '#a78bfa', type: 'main' },
    { id: 'math', label: 'Mathematics', x: 440, y: 80, r: 18, color: '#fbbf24', type: 'main' },
    { id: 'startup', label: 'Startup Building', x: 130, y: 280, r: 18, color: '#34d399', type: 'main' },
    { id: 'trading', label: 'Trading', x: 460, y: 270, r: 16, color: '#f87171', type: 'main' },
    { id: 'py', label: 'Python', x: 70, y: 50, r: 13, color: '#a78bfa', type: 'sub' },
    { id: 'ml', label: 'Machine Learning', x: 220, y: 30, r: 14, color: '#a78bfa', type: 'sub' },
    { id: 'uamil', label: 'UAMIL', x: 55, y: 230, r: 14, color: '#34d399', type: 'sub' },
    { id: 'rag', label: 'RAG', x: 65, y: 310, r: 12, color: '#22d3ee', type: 'sub' },
    { id: 'kg', label: 'Knowledge Graph', x: 175, y: 350, r: 13, color: '#4d9cff', type: 'sub' },
    { id: 'alg', label: 'Algorithms', x: 390, y: 30, r: 13, color: '#fbbf24', type: 'sub' },
    { id: 'stats', label: 'Statistics', x: 510, y: 110, r: 12, color: '#fbbf24', type: 'sub' },
    { id: 'quant', label: 'Quant', x: 540, y: 230, r: 12, color: '#f87171', type: 'sub' },
  ];
  const edges = [
    ['root', 'ai'], ['root', 'math'], ['root', 'startup'], ['root', 'trading'],
    ['ai', 'py'], ['ai', 'ml'], ['startup', 'uamil'], ['startup', 'rag'], ['startup', 'kg'],
    ['math', 'alg'], ['math', 'stats'], ['trading', 'quant'], ['ai', 'kg'],
  ];

  return (
    <div className="content">
      <div className="content-header">
        <h2>Knowledge Graph</h2>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button className="action-btn secondary">Export</button>
          <button className="action-btn primary">+ Add Node</button>
        </div>
      </div>
      <div className="kg-page-grid">
        <div className="kg-canvas">
          <svg ref={svgRef} className="kg-svg" viewBox="0 0 600 400">
            <defs>
              <filter id="glow">
                <feGaussianBlur stdDeviation="2" result="blur" />
                <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
              </filter>
            </defs>
            {edges.map(([a, b], i) => {
              const na = nodes.find(n => n.id === a);
              const nb = nodes.find(n => n.id === b);
              return <line key={i} x1={na.x} y1={na.y} x2={nb.x} y2={nb.y} stroke="rgba(255,255,255,0.07)" strokeWidth="1.5" />;
            })}
            {nodes.map(n => (
              <g key={n.id} style={{ cursor: 'pointer' }}>
                <circle cx={n.x} cy={n.y} r={n.r + 4} fill={n.color} opacity="0.06" />
                <circle cx={n.x} cy={n.y} r={n.r} fill={n.color} opacity={n.type === 'root' ? 0.9 : 0.7} />
                <text x={n.x} y={n.y + n.r + 12} textAnchor="middle" fontSize={n.type === 'root' ? 11 : 9.5} fill="rgba(255,255,255,0.65)" fontFamily="DM Sans">{n.label}</text>
                {n.type === 'root' && <text x={n.x} y={n.y + 4} textAnchor="middle" fontSize="11" fill="#fff" fontFamily="Syne" fontWeight="700">P</text>}
              </g>
            ))}
          </svg>
        </div>
        <div className="right-panel">
          <div className="rp-section">
            <div className="rp-title">Top Topics</div>
            {[
              { label: 'AI Engineering', val: '312 nodes', color: '#a78bfa' },
              { label: 'Mathematics', val: '189 nodes', color: '#fbbf24' },
              { label: 'Startup Building', val: '156 nodes', color: '#34d399' },
              { label: 'Trading', val: '98 nodes', color: '#f87171' },
              { label: 'Research', val: '94 nodes', color: '#4d9cff' },
            ].map((item, i) => (
              <div key={i} className="rp-item">
                <div className="rp-item-dot" style={{ background: item.color }}></div>
                <span>{item.label}</span>
                <span className="rp-item-val">{item.val}</span>
              </div>
            ))}
          </div>
          <div className="rp-section">
            <div className="rp-title">Graph Stats</div>
            {[
              { label: 'Total Nodes', val: '2,413' },
              { label: 'Connections', val: '4,829' },
              { label: 'Depth', val: '6 levels' },
              { label: 'Last Updated', val: '2 min ago' },
            ].map((s, i) => (
              <div key={i} className="rp-item">
                <span>{s.label}</span>
                <span className="rp-item-val">{s.val}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
