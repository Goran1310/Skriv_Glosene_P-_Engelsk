import React, { useState } from 'react';
import './AddVocabulary.css';

function AddVocabulary({ onNavigate, vocabulary, saveVocabulary, language, languageLabel }) {
  const [week, setWeek] = useState('');
  const [words, setWords] = useState('');
  const [wordCount, setWordCount] = useState(0);

  const handleWordsChange = (e) => {
    const text = e.target.value;
    setWords(text);
    const lines = text.trim().split('\n').filter(line => line.trim());
    setWordCount(lines.length);
  };

  const handleSave = () => {
    if (!week || !words.trim()) {
      alert('Vennligst fyll inn uke og ord! ✍️');
      return;
    }

    const weekNum = parseInt(week);
    if (isNaN(weekNum)) {
      alert('Uke må være et tall! 🔢');
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
        alert(`Line looks weird:\n"${line}"\n\nUse: ${languageLabel.toLowerCase()} → norsk`);
        return;
      }

      if (parts.length === 2) {
        const foreignWord = parts[0].trim();
        const norwegian = parts[1].trim();
        newVocab.push({ week: weekNum, [language]: foreignWord, norwegian });
      }
    }

    if (newVocab.length === 0) {
      alert('Ingen gyldige ord funnet! ✍️');
      return;
    }

    saveVocabulary([...vocabulary, ...newVocab]);
    setWeek('');
    setWords('');
    setWordCount(0);
    alert(`🎉 Perfekt!\n\nLa til ${newVocab.length} ord i uke ${weekNum}!`);
    onNavigate('menu');
  };

  const handleCancel = () => {
    if (words.trim() && !window.confirm('Gå tilbake uten å lagre? 🤔')) {
      return;
    }
    onNavigate('menu');
  };

  const weeks = [...new Set(vocabulary.map(v => v.week))].sort((a, b) => a - b);

  return (
    <div className="add-vocabulary">
      <h1>➕ Legg til nye ord</h1>

      <div className="form-container">
        <div className="week-section">
          <label className="section-label">📅 Velg uke</label>
          <div className="week-input-group">
            <input
              type="number"
              value={week}
              onChange={(e) => setWeek(e.target.value)}
              placeholder="Uke nummer"
              className="week-input"
              min="1"
              max="52"
            />
            {weeks.length > 0 && (
              <div className="week-quick-select">
                <span className="quick-label">Eller velg:</span>
                {weeks.slice(-7).map(w => (
                  <button
                    key={w}
                    onClick={() => setWeek(w.toString())}
                    className={`week-btn ${week === w.toString() ? 'active' : ''}`}
                  >
                    {w}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="words-section">
          <label className="section-label">
            ✍️ Skriv ord (ett par per linje)
            {wordCount > 0 && <span className="word-count">{wordCount} ord</span>}
          </label>
          <div className="format-help">
            <strong>Format:</strong> <code>{languageLabel.toLowerCase()} → norsk</code>
            <div className="examples">
              <div className="example">✓ happy → glad</div>
              <div className="example">✓ for instance → for eksempel</div>
              <div className="example">✓ crooked → skeive</div>
            </div>
          </div>
          <textarea
            value={words}
            onChange={handleWordsChange}
            placeholder="happy → glad
sad → trist
for instance → for eksempel"
            rows={14}
            className="words-textarea"
            autoFocus
          />
        </div>

        <div className="button-group">
          <button onClick={handleSave} className="save-btn" disabled={!week || !words.trim()}>
            💾 Lagre ord
          </button>
          <button onClick={handleCancel} className="cancel-btn">
            ❌ Avbryt
          </button>
        </div>
      </div>

      <button onClick={() => onNavigate('menu')} className="back-button">
        ⬅️ Tilbake til meny
      </button>
    </div>
  );
}

export default AddVocabulary;
