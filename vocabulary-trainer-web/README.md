# Vocabulary Trainer

Norwegian-English vocabulary learning application with quiz functionality.

**Live App:** https://effortless-bombolone-a7184d.netlify.app/

## 🚀 Quick Deployment

To deploy changes to Netlify, simply run from the parent directory:

```powershell
.\deploy.ps1
```

Or with a custom commit message:

```powershell
.\deploy.ps1 -Message "Added new vocabulary words"
```

**What it does:**
1. Builds the React app (`npm run build`)
2. Commits all changes with timestamp
3. Pushes to GitHub
4. Triggers automatic Netlify deployment (1-3 minutes)

## 📝 Adding New Vocabulary

**IMPORTANT:** Edit ONLY `public/preload-vocabulary.js` to add new words:

```javascript
{ week: 3, norwegian: "word", english: "translation" }
```

This is the **single source of truth** for vocabulary data. Do NOT edit `public/index.html` directly.

Then run `.\deploy.ps1` to deploy.

## 🔄 LocalStorage Versioning

The app uses **localStorage versioning** to handle data persistence issues when deploying updates.

### Why This Matters

**Problem:** localStorage is persistent by design
- Browser keeps data until explicitly cleared
- Deploying new React code doesn't touch existing localStorage keys
- Service Workers and aggressive caching can cause old data to persist
- Even hard refresh may not help

**Result:**
- App updates but old cached/stored data remains
- Schema changes can cause errors
- Users may see outdated interface or broken features

### How We Fixed It ✅

The app now checks version on every load:

```javascript
const APP_VERSION = "1.2.0";

const storedVersion = localStorage.getItem('appVersion');

if (storedVersion !== APP_VERSION) {
  // Clear old data when app version changes
  localStorage.removeItem('vocabulary');
  localStorage.removeItem('scores');
  localStorage.setItem('appVersion', APP_VERSION);
}
```

**What happens:**
1. App loads and checks stored version
2. If version differs, old data is cleared
3. New version number is saved
4. Fresh start with new app structure

### When to Update Version

Increment `APP_VERSION` in `src/App.js` when you:
- ✅ Change localStorage data structure
- ✅ Add/remove localStorage keys
- ✅ Change vocabulary schema
- ✅ Deploy breaking changes

**Example:**
```javascript
// Before deployment with schema change
const APP_VERSION = "1.2.0";  // Change to "1.3.0"
```

Then `.\deploy.ps1` - all users will get fresh data on next visit.

### Data Preserved

- ❌ **Cleared on version change:** vocabulary, scores (app data)
- ✅ **Preserved:** username (user preference)

You can customize what gets cleared vs. preserved in `App.js` line 25-30.

## 🌐 Deployment Setup

The app is automatically deployed to Netlify via GitHub integration:
- **Repository:** https://github.com/Goran1310/Skriv_Glosene_P-_Engelsk
- **Netlify Config:** `../netlify.toml`
- **Build Command:** `npm run build`
- **Publish Directory:** `build/`

Every push to `main` branch triggers a new deployment automatically.

---

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
