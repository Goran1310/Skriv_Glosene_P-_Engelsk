import React from 'react';
import './MainMenu.css';

function MainMenu({ onNavigate, vocabulary }) {
  const weeks = [...new Set(vocabulary.map(v => v.week))].sort((a, b) => a - b);
  const totalWords = vocabulary.length;

  return (
    <div className="main-menu">
      <div className="header">
        <h1>🌟 Vocabulary Trainer! 🌟</h1>
      </div>

      <div className="welcome">
        <h2>Welcome! 👋</h2>
      </div>

      <div className="button-grid">
        <button className="menu-button add-btn" onClick={() => onNavigate('add')}>
          📝 Add New Words
        </button>
        <button className="menu-button view-btn" onClick={() => onNavigate('view')}>
          👀 View My Words
        </button>
        <button className="menu-button quiz-btn" onClick={() => onNavigate('quiz')}>
          🎮 Take a Quiz!
        </button>
        <button className="menu-button results-btn" onClick={() => onNavigate('results')}>
          📊 My Scores
        </button>
        <button className="menu-button settings-btn" onClick={() => onNavigate('settings')}>
          ⚙️ Settings
        </button>
      </div>

      <div className="stats-footer">
        <p>📚 Weeks: {weeks.length} | 📖 Total Words: {totalWords}</p>
      </div>
    </div>
  );
}

export default MainMenu;
