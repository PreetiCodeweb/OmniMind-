const { useState, useEffect, useRef } = React;

const ChatView = () => {
  const [messages, setMessages] = useState(CHAT_HISTORY);
  const [input, setInput] = useState('');
  const [activeModel, setActiveModel] = useState('claude');
  const [typing, setTyping] = useState(false);
  const [memoryCapture, setMemoryCapture] = useState(false);
  const messagesEnd = useRef(null);
  const [toast, setToast] = useState(null);

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  };

  const send = () => {
    if (!input.trim()) return;
    const userMsg = {
      id: Date.now(),
      role: 'user',
      text: input,
      time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setTyping(true);

    setTimeout(() => {
      setTyping(false);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'ai',
          model: activeModel === 'claude' ? 'Claude' : activeModel === 'gemini' ? 'Gemini' : 'GPT-4o',
          modelColor: activeModel === 'claude' ? '#34d399' : activeModel === 'gemini' ? '#4d9cff' : '#a78bfa',
          text: 'I have your full project context loaded from your AI Passport and Memory Vault. Based on your previous sessions, here\'s my response — continuing from where we left off without you needing to explain anything again.',
          time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
        },
      ]);
      if (memoryCapture) showToast('✦ 1 new memory captured from this exchange');
    }, 1800);
  };

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, typing]);

  return (
    <div className="chat-wrap">
      <div style={{ padding: '12px 20px', borderBottom: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', gap: '8px', background: 'var(--bg-base)' }}>
        <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Active model:</span>
        {MODELS.slice(0, 3).map(m => (
          <div key={m.id} className={`input-chip ${activeModel === m.id ? 'active' : ''}`} onClick={() => setActiveModel(m.id)}>
            <div className="chip-dot" style={{ background: m.dot }}></div>
            {m.name}
          </div>
        ))}
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Memory capture</span>
          <label className="toggle">
            <input type="checkbox" checked={memoryCapture} onChange={(e) => setMemoryCapture(e.target.checked)} />
            <span className="toggle-slider"></span>
          </label>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map(msg => (
          <div key={msg.id} className={`msg ${msg.role}`}>
            {msg.role === 'ai' && (
              <div className="msg-avatar" style={{ background: `${msg.modelColor}20`, color: msg.modelColor, fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: '10px' }}>
                {msg.model?.[0]}
              </div>
            )}

            <div>
              <div className="msg-bubble" style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</div>
              {msg.role === 'ai' && (
                <div className="msg-model">
                  <span className="model-pill" style={{ background: `${msg.modelColor}20`, color: msg.modelColor }}>{msg.model}</span>
                  <span>{msg.time}</span>
                  <span style={{ marginLeft: '4px', fontSize: '10px', color: 'var(--text-muted)' }}>· Memory synced ✓</span>
                </div>
              )}
              {msg.role === 'user' && <div className="msg-model" style={{ justifyContent: 'flex-end' }}>{msg.time}</div>}
            </div>

            {msg.role === 'user' && (
              <div className="msg-avatar" style={{ background: 'rgba(77,156,255,0.2)', color: 'var(--accent-blue)', fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: '11px' }}>P</div>
            )}
          </div>
        ))}

        {typing && (
          <div className="msg ai">
            <div className="msg-avatar" style={{ background: 'rgba(52,211,153,0.2)', color: '#34d399', fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: '10px' }}>C</div>
            <div className="msg-bubble" style={{ minWidth: '60px' }}>
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
            </div>
          </div>
        )}
        <div ref={messagesEnd} />
      </div>

      <div className="chat-input-area">
        <div className="chat-input-wrap">
          <textarea
            className="chat-input"
            placeholder="Message your AI — with full memory context..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }}
            rows={1}
          />
          <button className="send-btn" onClick={send} disabled={!input.trim()}>➤</button>
        </div>
        <div style={{ display: 'flex', gap: '6px', marginTop: '8px', flexWrap: 'wrap' }}>
          {['Continue last session', 'Summarize project', 'Draft code skeleton', 'What have I learned?'].map(s => (
            <div key={s} className="input-chip" onClick={() => setInput(s)} style={{ fontSize: '11px', cursor: 'pointer' }}>{s}</div>
          ))}
        </div>
      </div>

      {toast && <div className="toast">{toast}</div>}
    </div>
  );
};
