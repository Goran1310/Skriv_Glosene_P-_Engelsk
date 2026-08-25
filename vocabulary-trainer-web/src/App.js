import React, { useState, useEffect } from 'react';
import './App.css';
import MainMenu from './components/MainMenu';
import AddVocabulary from './components/AddVocabulary';
import ViewVocabulary from './components/ViewVocabulary';
import Quiz from './components/Quiz';
import Results from './components/Results';
import Settings from './components/Settings';

const GRADES = [4, 5, 6, 7, 8, 9, 10];
const DEFAULT_GRADE = 7;
const LANGUAGES = [
  { id: 'english', label: 'Engelsk' },
  { id: 'french', label: 'Fransk' },
];
const DEFAULT_LANGUAGE = 'english';

function App() {
  const [currentScreen, setCurrentScreen] = useState('menu');
  const [username, setUsername] = useState('Student');
  const [selectedGrade, setSelectedGrade] = useState(DEFAULT_GRADE);
  const [selectedLanguage, setSelectedLanguage] = useState(DEFAULT_LANGUAGE);
  const [vocabulary, setVocabulary] = useState([]);
  const [scores, setScores] = useState([]);

  // Load data from localStorage on mount (preload-vocabulary.js already merged any new words in)
  useEffect(() => {
    const savedGrade = parseInt(localStorage.getItem('selectedGrade'), 10);
    const grade = GRADES.includes(savedGrade) ? savedGrade : DEFAULT_GRADE;
    const savedLanguage = localStorage.getItem('selectedLanguage');
    const language = LANGUAGES.some(l => l.id === savedLanguage) ? savedLanguage : DEFAULT_LANGUAGE;

    // One-time migration: pre-language versions stored data under 'vocabulary_grade{N}' (English only)
    const legacyKey = `vocabulary_grade${grade}`;
    const englishKey = `vocabulary_grade${grade}_english`;
    if (localStorage.getItem(legacyKey) && !localStorage.getItem(englishKey)) {
      localStorage.setItem(englishKey, localStorage.getItem(legacyKey));
    }

    const savedVocab = localStorage.getItem(`vocabulary_grade${grade}_${language}`);
    const savedScores = localStorage.getItem('scores');
    const savedUsername = localStorage.getItem('username');

    setSelectedGrade(grade);
    setSelectedLanguage(language);
    if (savedVocab) setVocabulary(JSON.parse(savedVocab));
    if (savedScores) setScores(JSON.parse(savedScores));
    if (savedUsername) setUsername(savedUsername);
  }, []);

  // Switch grade: persist the choice and load that grade's vocabulary (cached, no need to reselect)
  const selectGrade = (grade) => {
    setSelectedGrade(grade);
    localStorage.setItem('selectedGrade', grade);
    const savedVocab = localStorage.getItem(`vocabulary_grade${grade}_${selectedLanguage}`);
    setVocabulary(savedVocab ? JSON.parse(savedVocab) : []);
  };

  // Switch language: persist the choice and load that language's vocabulary (cached, no need to reselect)
  const selectLanguage = (language) => {
    setSelectedLanguage(language);
    localStorage.setItem('selectedLanguage', language);
    const savedVocab = localStorage.getItem(`vocabulary_grade${selectedGrade}_${language}`);
    setVocabulary(savedVocab ? JSON.parse(savedVocab) : []);
  };

  // Save vocabulary to localStorage
  const saveVocabulary = (newVocab) => {
    setVocabulary(newVocab);
    localStorage.setItem(`vocabulary_grade${selectedGrade}_${selectedLanguage}`, JSON.stringify(newVocab));
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
        return (
          <MainMenu
            onNavigate={setCurrentScreen}
            vocabulary={vocabulary}
            grades={GRADES}
            selectedGrade={selectedGrade}
            onGradeChange={selectGrade}
            languages={LANGUAGES}
            selectedLanguage={selectedLanguage}
            onLanguageChange={selectLanguage}
          />
        );
      case 'add':
        return (
          <AddVocabulary
            onNavigate={setCurrentScreen}
            vocabulary={vocabulary}
            saveVocabulary={saveVocabulary}
            language={selectedLanguage}
            languageLabel={LANGUAGES.find(l => l.id === selectedLanguage).label}
          />
        );
      case 'view':
        return (
          <ViewVocabulary
            onNavigate={setCurrentScreen}
            vocabulary={vocabulary}
            language={selectedLanguage}
            languageLabel={LANGUAGES.find(l => l.id === selectedLanguage).label}
          />
        );
      case 'quiz':
        return (
          <Quiz
            onNavigate={setCurrentScreen}
            vocabulary={vocabulary}
            username={username}
            saveScore={saveScore}
            language={selectedLanguage}
            languageLabel={LANGUAGES.find(l => l.id === selectedLanguage).label}
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
        return (
          <MainMenu
            onNavigate={setCurrentScreen}
            vocabulary={vocabulary}
            grades={GRADES}
            selectedGrade={selectedGrade}
            onGradeChange={selectGrade}
            languages={LANGUAGES}
            selectedLanguage={selectedLanguage}
            onLanguageChange={selectLanguage}
          />
        );
    }
  };

  return (
    <div className="App">
      {renderScreen()}
    </div>
  );
}

export default App;
