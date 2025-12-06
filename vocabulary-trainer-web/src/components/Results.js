import React, { useState } from 'react';
import './Results.css';

function Results({ onNavigate, scores }) {
  const [filter, setFilter] = useState('all');

  const filteredScores = filter === 'all' 
    ? scores 
    : scores.filter(s => s.week === parseInt(filter));

  const weeks = [...new Set(scores.map(s => s.week))].sort((a, b) => a - b);

  const calculateStats = () => {
    if (filteredScores.length === 0) return null;

    const totalQuestions = filteredScores.reduce((sum, s) => sum + s.totalQuestions, 0);
    const totalCorrect = filteredScores.reduce((sum, s) => sum + s.correctAnswers, 0);
    const avgPercentage = Math.round(
      filteredScores.reduce((sum, s) => sum + s.percentage, 0) / filteredScores.length
    );
    const avgDuration = Math.round(
      filteredScores.reduce((sum, s) => sum + s.duration, 0) / filteredScores.length
    );

    return {
      totalTests: filteredScores.length,
      totalQuestions,
      totalCorrect,
      avgPercentage,
      avgDuration
    };
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('no-NO', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;
  };

  const stats = calculateStats();

  return (
    <div className="results">
      <h1>📊 Resultater</h1>

      <div className="filter-section">
        <label>
          Filter etter uke:
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="all">Alle uker</option>
            {weeks.map(week => (
              <option key={week} value={week}>Uke {week}</option>
            ))}
          </select>
        </label>
      </div>

      {stats && (
        <div className="stats-summary">
          <h2>📈 Statistikk</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Antall tester</div>
              <div className="stat-value">{stats.totalTests}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Gjennomsnitt</div>
              <div className="stat-value">{stats.avgPercentage}%</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Totalt spørsmål</div>
              <div className="stat-value">{stats.totalQuestions}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Riktige svar</div>
              <div className="stat-value">{stats.totalCorrect}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Gj.snitt tid</div>
              <div className="stat-value">{formatDuration(stats.avgDuration)}</div>
            </div>
          </div>
        </div>
      )}

      <div className="results-list">
        <h2>📝 Historikk</h2>
        {filteredScores.length === 0 ? (
          <div className="empty-message">
            Ingen resultater funnet {filter !== 'all' ? `for uke ${filter}` : ''}
          </div>
        ) : (
          <div className="results-table">
            {filteredScores.map((score, index) => (
              <div key={index} className="result-card">
                <div className="result-header">
                  <div className="result-date">{formatDate(score.date)}</div>
                  <div className="result-week">Uke {score.week === 'all' ? 'Alle' : score.week}</div>
                </div>
                <div className="result-details">
                  <div className="detail-item">
                    <span className="detail-label">Bruker:</span>
                    <span className="detail-value">{score.username}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Retning:</span>
                    <span className="detail-value">{score.direction}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Resultat:</span>
                    <span className="detail-value">
                      {score.correctAnswers} / {score.totalQuestions}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Prosent:</span>
                    <span className={`detail-value percentage ${
                      score.percentage >= 90 ? 'excellent' : 
                      score.percentage >= 70 ? 'good' : 
                      score.percentage >= 50 ? 'okay' : 'poor'
                    }`}>
                      {score.percentage}%
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Tid:</span>
                    <span className="detail-value">{formatDuration(score.duration)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <button onClick={() => onNavigate('menu')} className="back-button">
        ⬅️ Tilbake til meny
      </button>
    </div>
  );
}

export default Results;
