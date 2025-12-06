// Script to create all React component files
const fs = require('fs');
const path = require('path');

const componentsDir = path.join(__dirname, 'src', 'components');

// Component files content
const components = {
  'AddVocabulary.css': `.add-vocabulary {
  min-height: 100vh;
  background: #E8F4F8;
  padding: 20px;
}

.form-container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 30px;
  border-radius: 15px;
}

.week-selection {
  margin-bottom: 30px;
}

.week-input {
  width: 200px;
  padding: 10px;
  font-size: 1.1rem;
  text-align: center;
  border: 2px solid #4A90E2;
  border-radius: 8px;
}

.existing-weeks {
  color: #666;
  font-size: 0.9rem;
  margin-top: 10px;
}

.words-input h3 {
  color: #2E5266;
}

.hint {
  color: #666;
  font-size: 0.9rem;
}

.words-textarea {
  width: 100%;
  padding: 15px;
  font-size: 1.1rem;
  border: 2px solid #4A90E2;
  border-radius: 8px;
  font-family: Arial, sans-serif;
}

.button-group {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 20px;
}

.button-group button {
  padding: 15px 30px;
  font-size: 1.1rem;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  color: white;
}

.save-btn { background: #50C878; }
.cancel-btn { background: #FFB347; }
.back-btn { background: #666; }`,

  'ViewVocabulary.js': `import React, { useState } from 'react';
import './ViewVocabulary.css';

function ViewVocabulary({ onNavigate, vocabulary }) {
  const weeks = [...new Set(vocabulary.map(v => v.week))].sort((a, b) => a - b);
  const [selectedWeek, setSelectedWeek] = useState(weeks[0] || null);

  const filteredWords = selectedWeek 
    ? vocabulary.filter(v => v.week === selectedWeek)
    : [];

  if (vocabulary.length === 0) {
    return (
      <div className="view-vocabulary">
        <div className="header">
          <h1>📚 My Word Lists 📚</h1>
        </div>
        <div className="empty-state">
          <h2>No words yet! 📝</h2>
          <p>Add some words first!</p>
          <button onClick={() => onNavigate('menu')} className="back-btn">
            ◀ Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="view-vocabulary">
      <div className="header">
        <h1>📚 My Word Lists 📚</h1>
      </div>

      <div className="content-container">
        <div className="week-selector">
          <h3>Select Week:</h3>
          {weeks.map(week => (
            <button
              key={week}
              onClick={() => setSelectedWeek(week)}
              className={\`week-btn \${selectedWeek === week ? 'active' : ''}\`}
            >
              Week {week} ({vocabulary.filter(v => v.week === week).length} words)
            </button>
          ))}
        </div>

        {selectedWeek && (
          <div className="word-table">
            <h2>Week {selectedWeek}</h2>
            <table>
              <thead>
                <tr>
                  <th>English</th>
                  <th>Norwegian</th>
                </tr>
              </thead>
              <tbody>
                {filteredWords.map((word, index) => (
                  <tr key={index}>
                    <td>{word.english}</td>
                    <td>{word.norwegian}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <button onClick={() => onNavigate('menu')} className="back-btn">
          ◀ Back
        </button>
      </div>
    </div>
  );
}

export default ViewVocabulary;`,

  'ViewVocabulary.css': `.view-vocabulary {
  min-height: 100vh;
  background: #E8F4F8;
  padding: 20px;
}

.content-container {
  max-width: 1000px;
  margin: 0 auto;
}

.week-selector {
  background: white;
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 20px;
}

.week-btn {
  display: block;
  width: 100%;
  padding: 15px;
  margin: 10px 0;
  border: 2px solid #4A90E2;
  background: white;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1.1rem;
}

.week-btn.active {
  background: #4A90E2;
  color: white;
}

.word-table {
  background: white;
  padding: 30px;
  border-radius: 15px;
  margin-bottom: 20px;
}

.word-table table {
  width: 100%;
  border-collapse: collapse;
}

.word-table th {
  background: #4A90E2;
  color: white;
  padding: 15px;
  text-align: left;
}

.word-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
}

.word-table tr:hover {
  background: #f5f5f5;
}

.empty-state {
  text-align: center;
  padding: 50px;
  background: white;
  border-radius: 15px;
  max-width: 600px;
  margin: 0 auto;
}`,

  'Quiz.js': `import React, { useState, useEffect } from 'react';
import './Quiz.css';

function Quiz({ onNavigate, vocabulary, username, saveScore }) {
  const [quizConfig, setQuizConfig] = useState(null);
  const [currentQ, setCurrentQ] = useState(0);
  const [questions, setQuestions] = useState([]);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState('');
  const [correct, setCorrect] = useState(0);
  const [showResult, setShowResult] = useState(false);
  const [startTime, setStartTime] = useState(null);

  const weeks = [...new Set(vocabulary.map(v => v.week))].sort((a, b) => a - b);

  const startQuiz = (week, direction, randomize) => {
    const vocabForWeek = vocabulary.filter(v => v.week === week);
    
    const qs = vocabForWeek.map(v => ({
      question: direction === 'NO→EN' ? v.norwegian : v.english,
      answer: direction === 'NO→EN' ? v.english : v.norwegian,
      direction
    }));

    if (randomize) {
      qs.sort(() => Math.random() - 0.5);
    }

    setQuestions(qs);
    setQuizConfig({ week, direction });
    setCurrentQ(0);
    setCorrect(0);
    setStartTime(Date.now());
  };

  const checkAnswer = () => {
    const userAnswer = answer.trim().toLowerCase();
    const correctAnswer = questions[currentQ].answer.toLowerCase();

    if (userAnswer === correctAnswer) {
      setFeedback('✅ Correct! Great job!');
      setCorrect(correct + 1);
    } else {
      setFeedback(\`❌ Oops! It was: \${questions[currentQ].answer}\`);
    }

    setTimeout(() => {
      if (currentQ + 1 < questions.length) {
        setCurrentQ(currentQ + 1);
        setAnswer('');
        setFeedback('');
      } else {
        finishQuiz();
      }
    }, 2000);
  };

  const finishQuiz = () => {
    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    const percentage = Math.round((correct / questions.length) * 100);
    
    const score = {
      username,
      date: new Date().toLocaleDateString(),
      time: new Date().toLocaleTimeString(),
      week: quizConfig.week,
      direction: quizConfig.direction,
      total: questions.length,
      correct,
      percentage,
      timeTaken
    };

    saveScore(score);
    setShowResult(true);
  };

  if (vocabulary.length === 0) {
    return (
      <div className="quiz">
        <div className="header">
          <h1>🎮 Quiz 🎮</h1>
        </div>
        <div className="empty-state">
          <h2>No words to quiz! 📝</h2>
          <button onClick={() => onNavigate('menu')} className="back-btn">
            ◀ Back
          </button>
        </div>
      </div>
    );
  }

  if (!quizConfig) {
    return (
      <div className="quiz">
        <div className="header">
          <h1>🎮 Quiz Setup 🎮</h1>
        </div>
        <div className="quiz-setup">
          <h2>Choose a week:</h2>
          {weeks.map(week => (
            <div key={week} className="week-option">
              <h3>Week {week}</h3>
              <p>{vocabulary.filter(v => v.week === week).length} words</p>
              <div className="direction-buttons">
                <button onClick={() => startQuiz(week, 'NO→EN', true)} className="direction-btn">
                  🇳🇴 Norwegian → English
                </button>
                <button onClick={() => startQuiz(week, 'EN→NO', true)} className="direction-btn">
                  🇬🇧 English → Norwegian
                </button>
              </div>
            </div>
          ))}
          <button onClick={() => onNavigate('menu')} className="back-btn">
            ◀ Back
          </button>
        </div>
      </div>
    );
  }

  if (showResult) {
    const percentage = Math.round((correct / questions.length) * 100);
    let emoji, msg;
    
    if (percentage === 100) {
      emoji = '🏆';
      msg = 'PERFECT! You\\'re amazing!';
    } else if (percentage >= 80) {
      emoji = '⭐';
      msg = 'Excellent work!';
    } else if (percentage >= 60) {
      emoji = '👍';
      msg = 'Good job!';
    } else {
      emoji = '💪';
      msg = 'Keep practicing!';
    }

    return (
      <div className="quiz">
        <div className="header">
          <h1>🎉 Quiz Complete! 🎉</h1>
        </div>
        <div className="quiz-result">
          <div className="emoji">{emoji}</div>
          <h2>{msg}</h2>
          <h3>Score: {correct}/{questions.length} ({percentage}%)</h3>
          <div className="button-group">
            <button onClick={() => setQuizConfig(null)} className="retry-btn">
              🔄 Quiz Again
            </button>
            <button onClick={() => onNavigate('menu')} className="menu-btn">
              🏠 Main Menu
            </button>
          </div>
        </div>
      </div>
    );
  }

  const hint = questions[currentQ].answer
    .split('')
    .map(c => c.match(/[a-z]/i) ? '_ ' : \`\${c} \`)
    .join('');

  return (
    <div className="quiz">
      <div className="header">
        <h1>🎯 Quiz Time! 🎯</h1>
      </div>
      <div className="quiz-container">
        <div className="progress">
          Question {currentQ + 1} of {questions.length} | Score: {correct}/{currentQ}
        </div>
        <div className="question-box">
          <div className="direction">{questions[currentQ].direction}</div>
          <div className="question">{questions[currentQ].question}</div>
          <div className="hint">{hint}</div>
          <input
            type="text"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && checkAnswer()}
            placeholder="Your answer"
            className="answer-input"
            autoFocus
          />
          <button onClick={checkAnswer} className="submit-btn">
            ✓ Check Answer
          </button>
          {feedback && <div className="feedback">{feedback}</div>}
        </div>
      </div>
    </div>
  );
}

export default Quiz;`,

  'Quiz.css': `.quiz {
  min-height: 100vh;
  background: #E8F4F8;
  padding: 20px;
}

.quiz-setup {
  max-width: 800px;
  margin: 0 auto;
}

.week-option {
  background: white;
  padding: 20px;
  margin: 20px 0;
  border-radius: 15px;
}

.direction-buttons {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.direction-btn {
  flex: 1;
  padding: 15px;
  border: 2px solid #4A90E2;
  background: white;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1.1rem;
}

.direction-btn:hover {
  background: #4A90E2;
  color: white;
}

.quiz-container {
  max-width: 800px;
  margin: 0 auto;
}

.progress {
  background: white;
  padding: 15px;
  text-align: center;
  border-radius: 10px;
  margin-bottom: 20px;
  font-size: 1.1rem;
  color: #2E5266;
}

.question-box {
  background: white;
  padding: 40px;
  border-radius: 15px;
  text-align: center;
}

.direction {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.question {
  font-size: 2rem;
  color: #4A90E2;
  margin: 20px 0;
  font-weight: bold;
}

.hint {
  font-family: 'Courier New', monospace;
  font-size: 1.2rem;
  color: #666;
  margin: 20px 0;
  letter-spacing: 2px;
}

.answer-input {
  width: 80%;
  padding: 15px;
  font-size: 1.3rem;
  text-align: center;
  border: 2px solid #4A90E2;
  border-radius: 10px;
  margin: 20px 0;
}

.submit-btn {
  padding: 15px 40px;
  font-size: 1.2rem;
  background: #50C878;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.feedback {
  font-size: 1.3rem;
  margin-top: 20px;
  font-weight: bold;
}

.quiz-result {
  max-width: 600px;
  margin: 0 auto;
  background: white;
  padding: 50px;
  border-radius: 15px;
  text-align: center;
}

.emoji {
  font-size: 5rem;
  margin: 20px 0;
}

.quiz-result h2 {
  color: #2E5266;
  margin: 20px 0;
}

.quiz-result h3 {
  color: #4A90E2;
  font-size: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 50px;
  background: white;
  border-radius: 15px;
  max-width: 600px;
  margin: 0 auto;
}`,

  'Results.js': `import React from 'react';
import './Results.css';

function Results({ onNavigate, scores, username }) {
  const userScores = scores.filter(s => s.username === username);
  
  const stats = userScores.reduce((acc, score) => {
    acc.totalQuizzes++;
    acc.totalCorrect += score.correct;
    acc.totalQuestions += score.total;
    if (score.percentage > acc.bestScore) acc.bestScore = score.percentage;
    return acc;
  }, { totalQuizzes: 0, totalCorrect: 0, totalQuestions: 0, bestScore: 0 });

  const avgScore = stats.totalQuestions > 0 
    ? Math.round((stats.totalCorrect / stats.totalQuestions) * 100)
    : 0;

  if (userScores.length === 0) {
    return (
      <div className="results">
        <div className="header">
          <h1>📊 My Scores 📊</h1>
        </div>
        <div className="empty-state">
          <h2>No quiz results yet! 🎮</h2>
          <p>Take a quiz to see your scores!</p>
          <button onClick={() => onNavigate('menu')} className="back-btn">
            ◀ Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="results">
      <div className="header">
        <h1>📊 My Scores 📊</h1>
      </div>

      <div className="content-container">
        <div className="stats-panel">
          <h2>📈 {username}'s Statistics</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-label">Total Quizzes:</div>
              <div className="stat-value">{stats.totalQuizzes}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Average Score:</div>
              <div className="stat-value">{avgScore}%</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Best Score:</div>
              <div className="stat-value">{stats.bestScore}%</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Total Questions:</div>
              <div className="stat-value">{stats.totalQuestions}</div>
            </div>
          </div>
        </div>

        <div className="scores-table">
          <h2>📜 Recent Quizzes (Last 10)</h2>
          <table>
            <thead>
              <tr>
                <th>📅 Date</th>
                <th>📚 Week</th>
                <th>🔄 Direction</th>
                <th>✓ Score</th>
                <th>⏱️ Time</th>
              </tr>
            </thead>
            <tbody>
              {userScores.slice(-10).reverse().map((score, index) => (
                <tr key={index}>
                  <td>{score.date}</td>
                  <td>Week {score.week}</td>
                  <td>{score.direction}</td>
                  <td>{score.correct}/{score.total} ({score.percentage}%)</td>
                  <td>{score.timeTaken || '-'}s</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <button onClick={() => onNavigate('menu')} className="back-btn">
          ◀ Back
        </button>
      </div>
    </div>
  );
}

export default Results;`,

  'Results.css': `.results {
  min-height: 100vh;
  background: #E8F4F8;
  padding: 20px;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
}

.stats-panel {
  background: white;
  padding: 30px;
  border-radius: 15px;
  margin-bottom: 20px;
}

.stats-panel h2 {
  color: #4A90E2;
  text-align: center;
  margin-bottom: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 10px;
}

.stat-label {
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #4A90E2;
}

.scores-table {
  background: white;
  padding: 30px;
  border-radius: 15px;
  margin-bottom: 20px;
  overflow-x: auto;
}

.scores-table h2 {
  color: #2E5266;
  margin-bottom: 20px;
}

.scores-table table {
  width: 100%;
  border-collapse: collapse;
}

.scores-table th {
  background: #4A90E2;
  color: white;
  padding: 12px;
  text-align: left;
}

.scores-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #ddd;
}

.scores-table tr:hover {
  background: #f5f5f5;
}`,

  'Settings.js': `import React, { useState } from 'react';
import './Settings.css';

function Settings({ onNavigate, username, saveUsername }) {
  const [name, setName] = useState(username);

  const handleSave = () => {
    if (name.trim()) {
      saveUsername(name.trim());
      alert('Settings saved! ✓');
      onNavigate('menu');
    } else {
      alert('Please enter a name!');
    }
  };

  return (
    <div className="settings">
      <div className="header">
        <h1>⚙️ Settings ⚙️</h1>
      </div>

      <div className="settings-container">
        <div className="settings-box">
          <h2>Your Name:</h2>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
            className="name-input"
          />
          <button onClick={handleSave} className="save-btn">
            💾 Save
          </button>
        </div>

        <button onClick={() => onNavigate('menu')} className="back-btn">
          ◀ Back
        </button>
      </div>
    </div>
  );
}

export default Settings;`,

  'Settings.css': `.settings {
  min-height: 100vh;
  background: #E8F4F8;
  padding: 20px;
}

.settings-container {
  max-width: 600px;
  margin: 0 auto;
}

.settings-box {
  background: white;
  padding: 40px;
  border-radius: 15px;
  margin-bottom: 20px;
  text-align: center;
}

.settings-box h2 {
  color: #2E5266;
  margin-bottom: 20px;
}

.name-input {
  width: 80%;
  padding: 15px;
  font-size: 1.2rem;
  text-align: center;
  border: 2px solid #4A90E2;
  border-radius: 10px;
  margin: 20px 0;
}

.save-btn {
  padding: 15px 40px;
  font-size: 1.2rem;
  background: #50C878;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.save-btn:hover {
  background: #45b368;
}`
};

// Write all files
Object.entries(components).forEach(([filename, content]) => {
  const filePath = path.join(componentsDir, filename);
  fs.writeFileSync(filePath, content);
  console.log(\`Created: \${filename}\`);
});

console.log('\\nAll component files created successfully!');
