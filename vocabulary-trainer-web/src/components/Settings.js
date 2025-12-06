import React from 'react';
import './Settings.css';

function Settings({ onNavigate, username, saveUsername }) {
  const [name, setName] = React.useState(username);

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

export default Settings;
