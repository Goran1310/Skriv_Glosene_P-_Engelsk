import React, { useState, useRef, useEffect } from 'react';
import './Quiz.css';

function Quiz({ onNavigate, vocabulary, username, saveScore }) {
  const [quizConfig, setQuizConfig] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [correctAnswers, setCorrectAnswers] = useState(0);
  const [showFeedback, setShowFeedback] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [quizFinished, setQuizFinished] = useState(false);
  const inputRef = useRef(null);

  const weeks = [...new Set(vocabulary.map(v => v.week))].sort((a, b) => a - b);

  const startQuiz = (week, direction, randomize) => {
    const vocabForWeek = week === 'all' 
      ? vocabulary 
      : vocabulary.filter(v => v.week === parseInt(week));

    if (vocabForWeek.length === 0) {
      alert('Ingen ord funnet for denne uken!');
      return;
    }

    let quizQuestions = vocabForWeek.map(v => ({
      question: direction === 'NO→EN' ? v.norwegian : v.english,
      answer: direction === 'NO→EN' ? v.english : v.norwegian,
      direction
    }));

    if (randomize) {
      quizQuestions = quizQuestions.sort(() => Math.random() - 0.5);
    }

    setQuestions(quizQuestions);
    setQuizConfig({ week, direction, randomize });
    setStartTime(Date.now());
    setCurrentQuestion(0);
    setCorrectAnswers(0);
    setQuizFinished(false);
  };

  const getHintText = () => {
    if (!questions[currentQuestion]) return '';
    const answer = questions[currentQuestion].answer;
    return '_'.repeat(answer.length);
  };

  const checkAnswer = () => {
    const correct = userAnswer.trim().toLowerCase() === 
                    questions[currentQuestion].answer.toLowerCase();
    
    setIsCorrect(correct);
    setShowFeedback(true);
    
    if (correct) {
      setCorrectAnswers(correctAnswers + 1);
      // Auto-advance only for correct answers
      setTimeout(() => {
        if (currentQuestion < questions.length - 1) {
          setCurrentQuestion(currentQuestion + 1);
          setUserAnswer('');
          setShowFeedback(false);
        } else {
          finishQuiz(correct);
        }
      }, 1500);
    }
  };

  const moveToNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setUserAnswer('');
      setShowFeedback(false);
    } else {
      finishQuiz(false);
    }
  };

  // Focus input field when question changes
  useEffect(() => {
    if (quizConfig && !showFeedback && inputRef.current) {
      inputRef.current.focus();
    }
  }, [currentQuestion, showFeedback, quizConfig]);

  const finishQuiz = (lastCorrect) => {
    const finalScore = correctAnswers + (lastCorrect ? 1 : 0);
    const duration = Math.floor((Date.now() - startTime) / 1000);
    const percentage = Math.round((finalScore / questions.length) * 100);
    
    saveScore({
      date: new Date().toISOString(),
      username,
      week: quizConfig.week,
      direction: quizConfig.direction,
      totalQuestions: questions.length,
      correctAnswers: finalScore,
      percentage,
      duration
    });

    setQuizFinished(true);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      if (showFeedback && !isCorrect) {
        // User pressed Enter after incorrect answer - move to next question
        moveToNextQuestion();
      } else if (!showFeedback && userAnswer.trim()) {
        // User pressed Enter to submit answer
        checkAnswer();
      }
    }
  };

  if (quizFinished) {
    const percentage = Math.round((correctAnswers / questions.length) * 100);
    return (
      <div className="quiz-finished">
        <h1>🎉 Quiz Fullført!</h1>
        <div className="quiz-results">
          <div className="result-item">
            <span className="result-label">Riktige svar:</span>
            <span className="result-value">{correctAnswers} / {questions.length}</span>
          </div>
          <div className="result-item">
            <span className="result-label">Prosent:</span>
            <span className="result-value">{percentage}%</span>
          </div>
          <div className="result-emoji">
            {percentage >= 90 ? '🌟' : percentage >= 70 ? '😊' : percentage >= 50 ? '😐' : '😕'}
          </div>
        </div>
        <button onClick={() => onNavigate('menu')} className="menu-button">
          🏠 Tilbake til meny
        </button>
        <button onClick={() => { setQuizConfig(null); setQuizFinished(false); }} className="retry-button">
          🔄 Nytt Quiz
        </button>
      </div>
    );
  }

  if (!quizConfig) {
    return (
      <div className="quiz-setup">
        <h1>📝 Quiz Oppsett</h1>
        
        <div className="setup-form">
          <div className="form-group">
            <label>Velg uke:</label>
            <select id="week-select" defaultValue="all">
              <option value="all">Alle uker</option>
              {weeks.map(week => (
                <option key={week} value={week}>Uke {week}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Retning:</label>
            <select id="direction-select" defaultValue="NO→EN">
              <option value="NO→EN">Norsk → Engelsk</option>
              <option value="EN→NO">Engelsk → Norsk</option>
            </select>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input type="checkbox" id="randomize-check" />
              Tilfeldig rekkefølge
            </label>
          </div>

          <button 
            onClick={() => {
              const week = document.getElementById('week-select').value;
              const direction = document.getElementById('direction-select').value;
              const randomize = document.getElementById('randomize-check').checked;
              startQuiz(week, direction, randomize);
            }}
            className="start-button"
          >
            ▶️ Start Quiz
          </button>
        </div>

        <button onClick={() => onNavigate('menu')} className="back-button">
          ⬅️ Tilbake
        </button>
      </div>
    );
  }

  return (
    <div className="quiz-active">
      <div className="quiz-header">
        <h2>Quiz: {quizConfig.direction}</h2>
        <div className="progress">
          Spørsmål {currentQuestion + 1} / {questions.length}
        </div>
      </div>

      <div className="quiz-card">
        <div className="question">
          {questions[currentQuestion]?.question}
        </div>

        <div className="input-wrapper">
          <div className="hint-overlay">{getHintText()}</div>
          <input
            ref={inputRef}
            type="text"
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
            onKeyPress={handleKeyPress}
            className="answer-input"
            disabled={showFeedback}
            autoFocus
          />
        </div>

        {!showFeedback && (
          <button 
            onClick={checkAnswer} 
            disabled={!userAnswer.trim()}
            className="submit-button"
          >
            ✅ Sjekk svar
          </button>
        )}

        {showFeedback && (
          <div className={`feedback ${isCorrect ? 'correct' : 'incorrect'}`}>
            {isCorrect ? (
              <>
                <span className="feedback-icon">✅</span>
                <span>Riktig!</span>
              </>
            ) : (
              <>
                <span className="feedback-icon">❌</span>
                <span>Feil. Riktig svar: {questions[currentQuestion].answer}</span>
                <div className="continue-hint">Trykk Enter for å fortsette</div>
              </>
            )}
          </div>
        )}
      </div>

      <div className="quiz-score">
        Poeng: {correctAnswers} / {currentQuestion + (showFeedback ? 1 : 0)}
      </div>
    </div>
  );
}

export default Quiz;
