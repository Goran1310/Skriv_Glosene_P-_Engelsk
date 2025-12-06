import React, { useState } from 'react';
import './ViewVocabulary.css';

function ViewVocabulary({ onNavigate, vocabulary, deleteVocabulary }) {
  const [selectedWeek, setSelectedWeek] = useState('all');

  const weeks = [...new Set(vocabulary.map(v => v.week))].sort((a, b) => a - b);
  const filteredVocab = selectedWeek === 'all' 
    ? vocabulary 
    : vocabulary.filter(v => v.week === parseInt(selectedWeek));

  const handleDelete = (index) => {
    const actualIndex = vocabulary.findIndex(v => v === filteredVocab[index]);
    if (window.confirm('Er du sikker på at du vil slette dette ordet?')) {
      deleteVocabulary(actualIndex);
    }
  };

  return (
    <div className="view-vocabulary">
      <h1>📚 Vis Ordliste</h1>
      
      <div className="controls">
        <label>
          Velg uke:
          <select value={selectedWeek} onChange={(e) => setSelectedWeek(e.target.value)}>
            <option value="all">Alle uker</option>
            {weeks.map(week => (
              <option key={week} value={week}>Uke {week}</option>
            ))}
          </select>
        </label>
        <div className="vocab-count">
          Totalt: {filteredVocab.length} ord
        </div>
      </div>

      <div className="vocabulary-table">
        <div className="table-header">
          <div>Uke</div>
          <div>Norsk</div>
          <div>Engelsk</div>
          <div>Handling</div>
        </div>
        {filteredVocab.map((item, index) => (
          <div key={index} className="table-row">
            <div className="week-cell">{item.week}</div>
            <div className="norwegian-cell">{item.norwegian}</div>
            <div className="english-cell">{item.english}</div>
            <div className="action-cell">
              <button onClick={() => handleDelete(index)} className="delete-btn">
                🗑️ Slett
              </button>
            </div>
          </div>
        ))}
        {filteredVocab.length === 0 && (
          <div className="empty-message">
            Ingen ord funnet {selectedWeek !== 'all' ? `for uke ${selectedWeek}` : ''}
          </div>
        )}
      </div>

      <button onClick={() => onNavigate('menu')} className="back-button">
        ⬅️ Tilbake til meny
      </button>
    </div>
  );
}

export default ViewVocabulary;
