import React from 'react';
import './MainMenu.css';

function MainMenu({ onNavigate, vocabulary, grades, selectedGrade, onGradeChange, languages, selectedLanguage, onLanguageChange }) {
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

      <div className="grade-selector">
        <label htmlFor="grade-select">🎓 Klasse:</label>
        <select
          id="grade-select"
          value={selectedGrade}
          onChange={(e) => onGradeChange(parseInt(e.target.value, 10))}
        >
          {grades.map(grade => (
            <option key={grade} value={grade}>{grade}. klasse</option>
          ))}
        </select>
      </div>

      <div className="grade-selector">
        <label htmlFor="language-select">🗣️ Språk:</label>
        <select
          id="language-select"
          value={selectedLanguage}
          onChange={(e) => onLanguageChange(e.target.value)}
        >
          {languages.map(lang => (
            <option key={lang.id} value={lang.id}>{lang.label}</option>
          ))}
        </select>
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
