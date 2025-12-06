import React, { useState } from 'react';
import './AddVocabulary.css';

function AddVocabulary({ onNavigate, vocabulary, saveVocabulary }) {
  const [week, setWeek] = useState('');
  const [words, setWords] = useState('');

  const handleSave = () => {
    if (!week || !words.trim()) {
      alert('Please enter a week number and some words! ✍️');
      return;
    }

    const weekNum = parseInt(week);
    if (isNaN(weekNum)) {
      alert('Week must be a number! 🔢');
      return;
    }

    const lines = words.trim().split('\n');
    const newVocab = [];
    
    for (let line of lines) {
      if (!line.trim()) continue;
      
      let parts;
      if (line.includes('→')) {
        parts = line.split('→');
      } else if (line.includes('\t')) {
        parts = line.split('\t');
      } else if (line.includes('  ')) {
        parts = line.split(/\s{2,}/);
      } else {
        alert(`Line looks weird:\n"${line}"\n\nUse: english → norwegian`);
        return;
      }

      if (parts.length === 2) {
        const english = parts[0].trim();
        const norwegian = parts[1].trim();
        newVocab.push({ week: weekNum, english, norwegian });
      }
    }

    if (newVocab.length === 0) {
      alert('No valid words found! ✍️');
      return;
    }

    saveVocabulary([...vocabulary, ...newVocab]);
    alert(`🎉 Awesome!\n\nAdded ${newVocab.length} words to Week ${weekNum}!`);
    onNavigate('menu');
  };

  const handleCancel = () => {
    if (words.trim() && !window.confirm('Go back without saving? 🤔')) {
      return;
    }
    onNavigate('menu');
  };

  const weeks = [...new Set(vocabulary.map(v => v.week))].sort((a, b) => a - b);

  return (
    <div className="add-vocabulary">
      <div className="header">
        <h1>📝 Add New Words 📝</h1>
      </div>

      <div className="form-container">
        <div className="week-selection">
          <h3>Which week? 📅</h3>
          <input
            type="number"
            value={week}
            onChange={(e) => setWeek(e.target.value)}
            placeholder="Week number"
            className="week-input"
          />
          {weeks.length > 0 && (
            <p className="existing-weeks">You have: {weeks.join(', ')}</p>
          )}
        </div>

        <div className="words-input">
          <h3>Type your words (one per line):</h3>
          <p className="hint">Format: english word → norwegian ord</p>
          <textarea
            value={words}
            onChange={(e) => setWords(e.target.value)}
            placeholder="happy → glad&#10;sad → trist&#10;for instance → for eksempel"
            rows={12}
            className="words-textarea"
          />
        </div>

        <div className="button-group">
          <button onClick={handleSave} className="save-btn">
            💾 Save Words
          </button>
          <button onClick={handleCancel} className="cancel-btn">
            ❌ Cancel
          </button>
          <button onClick={() => onNavigate('menu')} className="back-btn">
            ◀ Back
          </button>
        </div>
      </div>
    </div>
  );
}

export default AddVocabulary;
