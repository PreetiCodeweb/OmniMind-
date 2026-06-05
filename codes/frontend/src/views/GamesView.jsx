const { useState, useEffect } = React;

const games = [
  {
    id: 1,
    emoji: "🧠",
    title: "Brain Challenge",
    desc: "Solve quizzes, logic puzzles and coding questions.",
    tag: "Puzzle",
    color: "#6C63FF",
    glow: "rgba(108, 99, 255, 0.45)",
    accent: "#A89CFF",
    players: "12.4k",
    difficulty: "Medium",
  },
  {
    id: 2,
    emoji: "🚀",
    title: "AI Space Defender",
    desc: "Defend OmniMind servers from relentless cyber attacks.",
    tag: "Action",
    color: "#00D4FF",
    glow: "rgba(0, 212, 255, 0.45)",
    accent: "#7FECFF",
    players: "9.1k",
    difficulty: "Hard",
  },
  {
    id: 3,
    emoji: "🏃",
    title: "Cyber Runner",
    desc: "Collect data packets and dodge lethal malware streams.",
    tag: "Runner",
    color: "#FF6B6B",
    glow: "rgba(255, 107, 107, 0.45)",
    accent: "#FFAAAA",
    players: "21.7k",
    difficulty: "Easy",
    launchEndpoint: "http://localhost:8000/api/games/cyber-runner/start",
  },
];

const difficultyDot = { Easy: "#4ADE80", Medium: "#FACC15", Hard: "#F87171" };

function GameCard({ game, index }) {
  const [hovered, setHovered] = useState(false);
  const [launchState, setLaunchState] = useState("idle");

  const launchGame = async () => {
    if (!game.launchEndpoint) {
      setLaunchState("unavailable");
      setTimeout(() => setLaunchState("idle"), 1800);
      return;
    }

    setLaunchState("starting");

    try {
      const response = await fetch(game.launchEndpoint, { method: "POST" });
      if (!response.ok) {
        throw new Error("Launch failed");
      }
      setLaunchState("started");
    } catch (error) {
      setLaunchState("error");
    } finally {
      setTimeout(() => setLaunchState("idle"), 2400);
    }
  };

  const buttonLabel = {
    idle: "Play Now",
    starting: "Starting...",
    started: "Started",
    error: "Start Backend",
    unavailable: "Soon",
  }[launchState];

  return (
    <div
      className="game-card"
      style={{
        "--card-color": game.color,
        "--card-glow": game.glow,
        "--card-accent": game.accent,
        animationDelay: `${index * 0.12}s`,
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className="card-shimmer" />
      <div className="card-top-row">
        <span className="game-tag">{game.tag}</span>
        <span className="player-count">👥 {game.players}</span>
      </div>

      <div className={`emoji-wrap ${hovered ? "bounce" : ""}`}>
        <span className="game-emoji">{game.emoji}</span>
      </div>

      <h3 className="game-title">{game.title}</h3>
      <p className="game-desc">{game.desc}</p>

      <div className="card-footer">
        <span className="difficulty">
          <span
            className="diff-dot"
            style={{ background: difficultyDot[game.difficulty] }}
          />
          {game.difficulty}
        </span>
        <button
          className="play-btn"
          onClick={launchGame}
          disabled={launchState === "starting"}
        >
          <span className="btn-text">{buttonLabel}</span>
          <span className="btn-arrow">→</span>
        </button>
      </div>
    </div>
  );
}

function GamesView() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 50);
    return () => clearTimeout(t);
  }, []);

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');

        .games-view {
          min-height: 100vh;
          background: #080B14;
          font-family: 'DM Sans', sans-serif;
          padding: 72px 24px 80px;
          position: relative;
          overflow: hidden;
        }

        /* Radial background glow blobs */
        .games-view::before {
          content: '';
          position: fixed;
          top: -200px; left: 50%;
          transform: translateX(-50%);
          width: 800px; height: 500px;
          background: radial-gradient(ellipse, rgba(108,99,255,0.12) 0%, transparent 70%);
          pointer-events: none;
        }

        /* Grid pattern overlay */
        .games-view::after {
          content: '';
          position: fixed;
          inset: 0;
          background-image:
            linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
          background-size: 48px 48px;
          pointer-events: none;
          mask-image: radial-gradient(ellipse 80% 60% at 50% 0%, black 30%, transparent 100%);
        }

        /* ── Header ── */
        .games-header {
          text-align: center;
          margin-bottom: 64px;
          position: relative;
          z-index: 1;
          opacity: 0;
          transform: translateY(24px);
          transition: opacity 0.6s ease, transform 0.6s ease;
        }
        .games-header.visible {
          opacity: 1;
          transform: translateY(0);
        }

        .eyebrow {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          font-size: 11px;
          font-weight: 600;
          letter-spacing: 0.18em;
          text-transform: uppercase;
          color: #6C63FF;
          border: 1px solid rgba(108,99,255,0.35);
          padding: 6px 14px;
          border-radius: 999px;
          margin-bottom: 20px;
          background: rgba(108,99,255,0.08);
        }
        .eyebrow-dot {
          width: 6px; height: 6px;
          border-radius: 50%;
          background: #6C63FF;
          animation: pulse-dot 1.8s ease-in-out infinite;
        }
        @keyframes pulse-dot {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.4; transform: scale(0.7); }
        }

        .games-header h1 {
          font-family: 'Syne', sans-serif;
          font-size: clamp(36px, 7vw, 64px);
          font-weight: 800;
          color: #F0F0FF;
          line-height: 1.05;
          margin: 0 0 12px;
          letter-spacing: -0.02em;
        }
        .games-header h1 span {
          background: linear-gradient(120deg, #6C63FF, #00D4FF 60%, #FF6B6B);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .games-header p {
          font-size: 17px;
          color: rgba(200, 200, 230, 0.55);
          margin: 0 auto;
          max-width: 420px;
          line-height: 1.6;
        }

        /* ── Grid ── */
        .games-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 24px;
          max-width: 1020px;
          margin: 0 auto;
          position: relative;
          z-index: 1;
        }

        /* ── Card ── */
        .game-card {
          background: rgba(255,255,255,0.035);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 20px;
          padding: 28px 26px 24px;
          position: relative;
          overflow: hidden;
          cursor: pointer;
          opacity: 0;
          transform: translateY(32px);
          animation: card-in 0.55s cubic-bezier(0.22,1,0.36,1) forwards;
          transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        }
        @keyframes card-in {
          to { opacity: 1; transform: translateY(0); }
        }
        .game-card:hover {
          transform: translateY(-6px);
          box-shadow: 0 24px 56px var(--card-glow), 0 0 0 1px var(--card-color);
          border-color: var(--card-color);
        }

        /* Shimmer top-edge accent */
        .card-shimmer {
          position: absolute;
          top: 0; left: 0; right: 0;
          height: 2px;
          background: linear-gradient(90deg, transparent, var(--card-color), transparent);
          opacity: 0;
          transition: opacity 0.3s ease;
        }
        .game-card:hover .card-shimmer { opacity: 1; }

        /* Glow orb behind emoji */
        .game-card::before {
          content: '';
          position: absolute;
          top: -30px; right: -30px;
          width: 140px; height: 140px;
          border-radius: 50%;
          background: var(--card-glow);
          filter: blur(40px);
          opacity: 0;
          transition: opacity 0.4s ease;
          pointer-events: none;
        }
        .game-card:hover::before { opacity: 1; }

        .card-top-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 22px;
        }

        .game-tag {
          font-size: 11px;
          font-weight: 600;
          letter-spacing: 0.12em;
          text-transform: uppercase;
          color: var(--card-color);
          background: rgba(255,255,255,0.06);
          border: 1px solid rgba(255,255,255,0.1);
          padding: 4px 10px;
          border-radius: 999px;
        }

        .player-count {
          font-size: 12px;
          color: rgba(200,200,230,0.45);
          font-weight: 500;
        }

        .emoji-wrap {
          width: 62px; height: 62px;
          border-radius: 16px;
          background: rgba(255,255,255,0.06);
          display: flex; align-items: center; justify-content: center;
          margin-bottom: 18px;
          border: 1px solid rgba(255,255,255,0.08);
          transition: transform 0.3s ease;
        }
        .emoji-wrap.bounce {
          animation: emoji-bounce 0.4s cubic-bezier(0.34,1.56,0.64,1);
        }
        @keyframes emoji-bounce {
          0% { transform: scale(1); }
          50% { transform: scale(1.2) rotate(-5deg); }
          100% { transform: scale(1); }
        }

        .game-emoji { font-size: 28px; line-height: 1; }

        .game-title {
          font-family: 'Syne', sans-serif;
          font-size: 20px;
          font-weight: 700;
          color: #EEEEFF;
          margin: 0 0 10px;
          letter-spacing: -0.01em;
        }

        .game-desc {
          font-size: 14px;
          color: rgba(200,200,230,0.5);
          line-height: 1.65;
          margin: 0 0 24px;
        }

        .card-footer {
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .difficulty {
          display: flex;
          align-items: center;
          gap: 7px;
          font-size: 13px;
          color: rgba(200,200,230,0.5);
          font-weight: 500;
        }
        .diff-dot {
          width: 7px; height: 7px;
          border-radius: 50%;
          flex-shrink: 0;
        }

        .play-btn {
          display: flex;
          align-items: center;
          gap: 8px;
          background: var(--card-color);
          color: #fff;
          border: none;
          border-radius: 10px;
          padding: 10px 18px;
          font-size: 13px;
          font-weight: 600;
          font-family: 'DM Sans', sans-serif;
          cursor: pointer;
          position: relative;
          overflow: hidden;
          transition: opacity 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
          letter-spacing: 0.01em;
        }
        .play-btn::after {
          content: '';
          position: absolute;
          inset: 0;
          background: linear-gradient(to bottom, rgba(255,255,255,0.18), transparent);
          pointer-events: none;
        }
        .play-btn:hover {
          opacity: 0.92;
          transform: scale(1.04);
          box-shadow: 0 8px 24px var(--card-glow);
        }
        .play-btn:active { transform: scale(0.97); }
        .play-btn:disabled {
          cursor: wait;
          opacity: 0.7;
        }
        .btn-arrow {
          transition: transform 0.2s ease;
        }
        .play-btn:hover .btn-arrow { transform: translateX(3px); }
      `}</style>

      <div className="games-view">
        <div className={`games-header ${visible ? "visible" : ""}`}>
          <div className="eyebrow">
            <span className="eyebrow-dot" />
            OmniMind Games
          </div>
          <h1>
            Need a <span>Break?</span>
          </h1>
          <p>
            Step away from the chat and dive into mini-games built right into OmniMind.
          </p>
        </div>

        <div className="games-grid">
          {games.map((game, i) => (
            <GameCard key={game.id} game={game} index={i} />
          ))}
        </div>
      </div>
    </>
  );
}
