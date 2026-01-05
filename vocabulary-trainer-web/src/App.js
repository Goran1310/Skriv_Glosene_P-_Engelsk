import React, { useState, useEffect } from 'react';
import './App.css';
import MainMenu from './components/MainMenu';
import AddVocabulary from './components/AddVocabulary';
import ViewVocabulary from './components/ViewVocabulary';
import Quiz from './components/Quiz';
import Results from './components/Results';
import Settings from './components/Settings';

// App version for localStorage management
const APP_VERSION = "1.2.0";

function App() {
  const [currentScreen, setCurrentScreen] = useState('menu');
  const [username, setUsername] = useState('Student');
  const [vocabulary, setVocabulary] = useState([]);
  const [scores, setScores] = useState([]);

  // Load data from localStorage on mount with version checking
  useEffect(() => {
    // Check app version and clear old data if version changed
    const storedVersion = localStorage.getItem('appVersion');
    
    if (storedVersion !== APP_VERSION) {
      console.log(`App version changed from ${storedVersion || 'none'} to ${APP_VERSION}. Clearing old data...`);
      
      // Clear old localStorage data (you can migrate instead of removing)
      localStorage.removeItem('vocabulary');
      localStorage.removeItem('scores');
      // Keep username as it's user-specific
      // localStorage.removeItem('username');
      
      // Set new version
      localStorage.setItem('appVersion', APP_VERSION);
    }
    
    // Load data from localStorage
    const savedVocab = localStorage.getItem('vocabulary');
    const savedScores = localStorage.getItem('scores');
    const savedUsername = localStorage.getItem('username');
    
    if (savedVocab) setVocabulary(JSON.parse(savedVocab));
    if (savedScores) setScores(JSON.parse(savedScores));
    if (savedUsername) setUsername(savedUsername);
  }, []);

  // Save vocabulary to localStorage
  const saveVocabulary = (newVocab) => {
    setVocabulary(newVocab);
    localStorage.setItem('vocabulary', JSON.stringify(newVocab));
  };

  // Save scores to localStorage
  const saveScore = (score) => {
    const newScores = [...scores, score];
    setScores(newScores);
    localStorage.setItem('scores', JSON.stringify(newScores));
  };

  // Save username to localStorage
  const saveUsername = (name) => {
    setUsername(name);
    localStorage.setItem('username', name);
  };

  const renderScreen = () => {
    switch (currentScreen) {
      case 'menu':
        return <MainMenu onNavigate={setCurrentScreen} vocabulary={vocabulary} />;
      case 'add':
        return (
          <AddVocabulary
            onNavigate={setCurrentScreen}
            vocabulary={vocabulary}
            saveVocabulary={saveVocabulary}
          />
        );
      case 'view':
        return (
          <ViewVocabulary
            onNavigate={setCurrentScreen}
            vocabulary={vocabulary}
          />
        );
      case 'quiz':
        return (
          <Quiz
            onNavigate={setCurrentScreen}
            vocabulary={vocabulary}
            username={username}
            saveScore={saveScore}
          />
        );
      case 'results':
        return (
          <Results
            onNavigate={setCurrentScreen}
            scores={scores}
            username={username}
          />
        );
      case 'settings':
        return (
          <Settings
            onNavigate={setCurrentScreen}
            username={username}
            saveUsername={saveUsername}
          />
        );
      default:
        return <MainMenu onNavigate={setCurrentScreen} vocabulary={vocabulary} />;
    }
  };

  return (
    <div className="App">
      {renderScreen()}
    </div>
  );
}

export default App;
