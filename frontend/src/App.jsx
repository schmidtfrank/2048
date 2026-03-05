import { useState, useEffect, useCallback } from "react";

const TILE_COLORS = {
  0:    { bg: "#1a1a2e", text: "#1a1a2e", shadow: "none" },
  2:    { bg: "#e8f4f8", text: "#2d3748", shadow: "0 4px 15px rgba(232,244,248,0.3)" },
  4:    { bg: "#bee3f8", text: "#2d3748", shadow: "0 4px 15px rgba(190,227,248,0.4)" },
  8:    { bg: "#f6ad55", text: "#fff", shadow: "0 4px 20px rgba(246,173,85,0.6)" },
  16:   { bg: "#ed8936", text: "#fff", shadow: "0 4px 20px rgba(237,137,54,0.6)" },
  32:   { bg: "#fc8181", text: "#fff", shadow: "0 4px 20px rgba(252,129,129,0.7)" },
  64:   { bg: "#f56565", text: "#fff", shadow: "0 4px 25px rgba(245,101,101,0.8)" },
  128:  { bg: "#b794f4", text: "#fff", shadow: "0 4px 25px rgba(183,148,244,0.8)" },
  256:  { bg: "#9f7aea", text: "#fff", shadow: "0 4px 30px rgba(159,122,234,0.9)" },
  512:  { bg: "#7c3aed", text: "#fff", shadow: "0 4px 30px rgba(124,58,237,0.9)" },
  1024: { bg: "#48bb78", text: "#fff", shadow: "0 4px 35px rgba(72,187,120,0.9)" },
  2048: { bg: "#38a169", text: "#fff", shadow: "0 0 40px rgba(56,161,105,1), 0 0 80px rgba(56,161,105,0.5)" },
};

const getTileStyle = (value) => {
  const style = TILE_COLORS[value] || { bg: "#2d3748", text: "#fff", shadow: "0 4px 30px rgba(45,55,72,0.9)" };
  return style;
};

const getFontSize = (value) => {
  if (!value) return "1.8rem";
  const digits = String(value).length;
  if (digits <= 2) return "2rem";
  if (digits === 3) return "1.6rem";
  if (digits === 4) return "1.2rem";
  return "0.9rem";
};

function Tile({ value, isNew, isMerged }) {
  const style = getTileStyle(value);
  return (
    <div
      style={{
        background: style.bg,
        boxShadow: style.shadow,
        borderRadius: "12px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: getFontSize(value),
        fontFamily: "'Space Mono', monospace",
        fontWeight: "700",
        color: style.text,
        transition: "background 0.15s ease, box-shadow 0.15s ease",
        animation: isNew ? "popIn 0.18s cubic-bezier(0.175, 0.885, 0.32, 1.275)" :
                   isMerged ? "merge 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)" : "none",
        position: "relative",
        letterSpacing: "-0.02em",
      }}
    >
      {value !== 0 ? value : ""}
      {value === 2048 && (
        <div style={{
          position: "absolute",
          inset: 0,
          borderRadius: "12px",
          background: "radial-gradient(circle at 30% 30%, rgba(255,255,255,0.2) 0%, transparent 60%)",
          pointerEvents: "none",
        }} />
      )}
    </div>
  );
}

export default function App() {
  const [board, setBoard] = useState(Array(4).fill(null).map(() => Array(4).fill(0)));
  const [prevBoard, setPrevBoard] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | playing | loading
  const [score, setScore] = useState(0);
  const [newTiles, setNewTiles] = useState(new Set());
  const [mergedTiles, setMergedTiles] = useState(new Set());
  const [error, setError] = useState(null);

  const flatKey = (r, c) => r * 4 + c;

  const fetchScore = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/score");
      if (!res.ok) return;
      const data = await res.json();
      setScore(data.score ?? 0);
    } catch (_) {}
  };

  const applyBoard = (newBoard, oldBoard) => {
    const newSet = new Set();
    const mergeSet = new Set();

    if (oldBoard) {
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          const val = newBoard[r][c];
          if (val === 0) continue;
          if (oldBoard[r][c] === 0) newSet.add(flatKey(r, c));
          else if (val !== oldBoard[r][c]) mergeSet.add(flatKey(r, c));
        }
      }
    }

    setNewTiles(newSet);
    setMergedTiles(mergeSet);
    setTimeout(() => { setNewTiles(new Set()); setMergedTiles(new Set()); }, 300);

    setBoard(newBoard);
    fetchScore();
  };

  const startNewGame = useCallback(async () => {
    setStatus("loading");
    setError(null);
    try {
      const res = await fetch("http://127.0.0.1:8000/new");
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setNewTiles(new Set());
      setMergedTiles(new Set());
      setBoard(data.board);
      setPrevBoard(null);
      await fetchScore();
      setStatus("playing");
    } catch (e) {
      setError(e.message);
      setStatus("idle");
    }
  }, []);

  const sendMove = useCallback(async (key) => {
    if (status !== "playing") return;
    setStatus("loading");
    setError(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000/move/${key}`);
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setPrevBoard(board);
      applyBoard(data.board, board);
      setStatus("playing");
    } catch (e) {
      setError(e.message);
      setStatus("playing");
    }
  }, [status, board]);

  useEffect(() => {
    const handleKey = (e) => {
      const map = { w: "w", a: "a", s: "s", d: "d" };
      if (map[e.key]) {
        e.preventDefault();
        sendMove(map[e.key]);
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [sendMove]);

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0d0d1a",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "'Space Mono', monospace",
      padding: "24px",
      backgroundImage: `
        radial-gradient(ellipse at 20% 20%, rgba(124,58,237,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(56,161,105,0.06) 0%, transparent 50%)
      `,
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Bebas+Neue&display=swap');
        @keyframes popIn {
          0% { transform: scale(0); opacity: 0; }
          100% { transform: scale(1); opacity: 1; }
        }
        @keyframes merge {
          0% { transform: scale(1); }
          50% { transform: scale(1.18); }
          100% { transform: scale(1); }
        }
        @keyframes fadeSlideIn {
          from { opacity: 0; transform: translateY(-10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .new-game-btn {
          background: transparent;
          border: 1.5px solid rgba(124,58,237,0.6);
          color: #b794f4;
          padding: 10px 28px;
          font-family: 'Space Mono', monospace;
          font-size: 0.75rem;
          font-weight: 700;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s ease;
          position: relative;
          overflow: hidden;
        }
        .new-game-btn::before {
          content: '';
          position: absolute;
          inset: 0;
          background: rgba(124,58,237,0.1);
          opacity: 0;
          transition: opacity 0.2s;
        }
        .new-game-btn:hover::before { opacity: 1; }
        .new-game-btn:hover {
          border-color: rgba(124,58,237,0.9);
          color: #d6bcfa;
          box-shadow: 0 0 20px rgba(124,58,237,0.3);
        }
        .new-game-btn:active { transform: scale(0.97); }
        .new-game-btn:disabled { opacity: 0.4; cursor: not-allowed; }
      `}</style>

      {/* Header */}
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        width: "100%",
        maxWidth: "440px",
        marginBottom: "28px",
        animation: "fadeSlideIn 0.5s ease",
      }}>
        <div>
          <h1 style={{
            fontFamily: "'Bebas Neue', sans-serif",
            fontSize: "3.5rem",
            color: "#fff",
            margin: 0,
            letterSpacing: "0.05em",
            lineHeight: 1,
          }}>2048</h1>
          <div style={{
            color: "rgba(255,255,255,0.3)",
            fontSize: "0.65rem",
            letterSpacing: "0.15em",
            textTransform: "uppercase",
            marginTop: "2px",
          }}>
            use W A S D to move
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: "10px" }}>
          <div style={{
            background: "rgba(255,255,255,0.04)",
            border: "1px solid rgba(255,255,255,0.08)",
            borderRadius: "8px",
            padding: "8px 18px",
            textAlign: "center",
          }}>
            <div style={{ fontSize: "0.6rem", color: "rgba(255,255,255,0.35)", letterSpacing: "0.15em", textTransform: "uppercase" }}>Score</div>
            <div style={{ fontSize: "1.3rem", fontWeight: "700", color: "#b794f4" }}>{score}</div>
          </div>
          <button className="new-game-btn" onClick={startNewGame} disabled={status === "loading"}>
            {status === "loading" ? "···" : "New Game"}
          </button>
        </div>
      </div>

      {/* Board */}
      <div style={{
        background: "rgba(255,255,255,0.03)",
        border: "1px solid rgba(255,255,255,0.07)",
        borderRadius: "16px",
        padding: "12px",
        width: "100%",
        maxWidth: "440px",
        animation: "fadeSlideIn 0.5s ease 0.1s both",
        boxShadow: "0 20px 60px rgba(0,0,0,0.5)",
      }}>
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gridTemplateRows: "repeat(4, 1fr)",
          gap: "10px",
          aspectRatio: "1",
        }}>
          {/* col-major: board[col][row] → display at (row, col) */}
          {Array(4).fill(null).map((_, row) =>
            Array(4).fill(null).map((_, col) => {
              const value = board[row]?.[col] ?? 0;
              const key = flatKey(row, col);
              return (
                <Tile
                  key={`${row}-${col}`}
                  value={value}
                  isNew={newTiles.has(key)}
                  isMerged={mergedTiles.has(key)}
                />
              );
            })
          )}
        </div>
      </div>

      {/* Error */}
      {error && (
        <div style={{
          marginTop: "16px",
          padding: "10px 18px",
          background: "rgba(245,101,101,0.1)",
          border: "1px solid rgba(245,101,101,0.3)",
          borderRadius: "8px",
          color: "#fc8181",
          fontSize: "0.7rem",
          letterSpacing: "0.05em",
          maxWidth: "440px",
          width: "100%",
          animation: "fadeSlideIn 0.3s ease",
        }}>
          ⚠ {error}
        </div>
      )}

      {/* Idle prompt */}
      {status === "idle" && !error && (
        <div style={{
          marginTop: "16px",
          color: "rgba(255,255,255,0.2)",
          fontSize: "0.7rem",
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          animation: "fadeSlideIn 0.5s ease 0.3s both",
        }}>
          Press New Game to start
        </div>
      )}
    </div>
  );
}