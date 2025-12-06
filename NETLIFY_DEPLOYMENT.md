# Deployment Guide for Netlify

## Important Note ⚠️

This is a **Python desktop application** that uses tkinter for the GUI. It **cannot be directly deployed to Netlify** as-is because:
- Netlify hosts static websites and serverless functions
- This app requires Python runtime and tkinter GUI library
- Desktop applications need to run locally on the user's computer

## Deployment Options

### Option 1: Convert to Web Application (Recommended for Netlify)

To deploy on Netlify, you would need to convert this to a web application:

#### Steps:
1. **Create a web backend** using Flask or FastAPI:
   ```python
   # app.py
   from flask import Flask, render_template, request, jsonify
   from storage import VocabularyStorage, ScoreStorageJSON
   
   app = Flask(__name__)
   vocab_storage = VocabularyStorage()
   score_storage = ScoreStorageJSON()
   
   @app.route('/')
   def index():
       return render_template('index.html')
   
   @app.route('/api/quiz', methods=['GET'])
   def get_quiz():
       # API endpoint for quiz data
       pass
   ```

2. **Create web frontend** with HTML/CSS/JavaScript:
   ```html
   <!-- templates/index.html -->
   <!DOCTYPE html>
   <html>
   <head>
       <title>Skriv Glosene På Engelsk</title>
       <link rel="stylesheet" href="/static/style.css">
   </head>
   <body>
       <div id="app">
           <!-- Your web UI here -->
       </div>
       <script src="/static/app.js"></script>
   </body>
   </html>
   ```

3. **Deploy to Netlify**:
   - For static frontend: Deploy directly
   - For backend API: Use Netlify Functions or external service (Heroku, Railway, etc.)

### Option 2: Desktop Distribution (Current Version)

For distributing the **current desktop application**:

#### Windows Executable:
```powershell
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name="VocabularyTrainer" gui.py

# Executable will be in dist/VocabularyTrainer.exe
```

#### Cross-Platform Distribution:
1. **Share Python source code**:
   - Users need Python 3.7+ installed
   - Clone repository and run `python gui.py`

2. **Create installers**:
   - Windows: Use Inno Setup or NSIS
   - macOS: Create .app bundle with py2app
   - Linux: Create .deb or .rpm packages

### Option 3: GitHub Pages (Static Documentation)

You can deploy documentation and instructions to GitHub Pages:

1. **Create a landing page**:
   ```html
   <!-- docs/index.html -->
   <!DOCTYPE html>
   <html>
   <head>
       <title>Skriv Glosene På Engelsk</title>
   </head>
   <body>
       <h1>Norwegian-English Vocabulary Trainer</h1>
       <p>Download the desktop application:</p>
       <a href="https://github.com/goran1310/Skriv_Glosene_På_Engelsk/releases">
           Download Latest Release
       </a>
   </body>
   </html>
   ```

2. **Enable GitHub Pages**:
   - Go to repository Settings > Pages
   - Select source: main branch / docs folder
   - Your site will be at: `https://goran1310.github.io/Skriv_Glosene_På_Engelsk/`

## Quick Web Version (Static HTML)

If you want a simple web version without backend:

### Create index.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skriv Glosene På Engelsk</title>
    <style>
        body {
            font-family: 'Comic Sans MS', cursive;
            background: #E8F4F8;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            background: #4A90E2;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
        }
        .button {
            background: #50C878;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
        }
        .quiz-area {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🇳🇴 Skriv Glosene På Engelsk 🇬🇧</h1>
    </div>
    
    <div class="quiz-area">
        <h2>Vocabulary Quiz</h2>
        <p id="question">Loading...</p>
        <input type="text" id="answer" placeholder="Your answer">
        <button class="button" onclick="checkAnswer()">Check Answer</button>
        <p id="feedback"></p>
    </div>

    <script>
        // Vocabulary data (hardcoded for static version)
        const vocabulary = [
            {norwegian: "glad", english: "happy"},
            {norwegian: "trist", english: "sad"},
            // Add more words...
        ];
        
        let currentQuestion = 0;
        
        function loadQuestion() {
            const q = vocabulary[currentQuestion];
            document.getElementById('question').textContent = q.norwegian;
        }
        
        function checkAnswer() {
            const answer = document.getElementById('answer').value.toLowerCase();
            const correct = vocabulary[currentQuestion].english.toLowerCase();
            
            if (answer === correct) {
                document.getElementById('feedback').textContent = "✅ Correct!";
            } else {
                document.getElementById('feedback').textContent = `❌ Wrong. It was: ${correct}`;
            }
            
            currentQuestion = (currentQuestion + 1) % vocabulary.length;
            setTimeout(loadQuestion, 2000);
        }
        
        loadQuestion();
    </script>
</body>
</html>
```

### Deploy to Netlify:
```powershell
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd c:\Users\goran.lovincic\source\repos\Skriv_Glosene_På_Engelsk
netlify deploy --prod
```

## Recommended Approach

For **Netlify deployment**, I recommend:

1. **Keep the desktop app** in this repository
2. **Create a separate web version** using:
   - React/Vue.js for frontend
   - Store vocabulary in JSON files (no backend needed)
   - Use browser localStorage for scores
   - Deploy static site to Netlify

3. **OR use this repo for documentation**:
   - Host download links
   - User guides
   - Screenshots and demos

## Next Steps

1. **If you want the desktop app**: 
   - Push to GitHub: `git push -u origin main`
   - Create releases with executables
   - Share download link

2. **If you want web deployment**:
   - Let me know, and I'll help create a web version
   - Use separate repository or branch for web app

3. **For Netlify specifically**:
   - Create a simple landing page
   - Link to GitHub releases for downloads
   - Or convert to full web application

Would you like me to help with any of these options?
