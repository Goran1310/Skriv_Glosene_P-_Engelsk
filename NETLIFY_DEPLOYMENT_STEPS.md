# Netlify Deployment Steps 🚀

## Prerequisites
Your React app is ready and committed to git! ✅

## Option 1: Deploy via Netlify Dashboard (Easiest)

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `Skriv_Glosene_På_Engelsk`
3. Make it **Public** (required for free Netlify deployment)
4. **DO NOT** initialize with README, .gitignore, or license
5. Click "Create repository"

### Step 2: Push to GitHub
Run these commands in your terminal:
```powershell
cd 'c:\Users\goran.lovincic\source\repos\Skriv_Glosene_På_Engelsk'
git push -u origin main
```

### Step 3: Deploy to Netlify
1. Go to https://app.netlify.com/teams/goran1310/projects
2. Click **"Add new site"** → **"Import an existing project"**
3. Select **"Deploy with GitHub"**
4. Authorize Netlify to access your GitHub account
5. Select the repository: `goran1310/Skriv_Glosene_På_Engelsk`
6. Configure build settings:
   - **Base directory:** `vocabulary-trainer-web`
   - **Build command:** `npm run build`
   - **Publish directory:** `vocabulary-trainer-web/build`
7. Click **"Deploy site"**

Your app will be live in 2-3 minutes! 🎉

## Option 2: Deploy via Netlify CLI

### Step 1: Install Netlify CLI
```powershell
npm install -g netlify-cli
```

### Step 2: Login to Netlify
```powershell
netlify login
```

### Step 3: Deploy
```powershell
cd 'c:\Users\goran.lovincic\source\repos\Skriv_Glosene_På_Engelsk\vocabulary-trainer-web'
netlify init
# Follow the prompts:
# - Create & configure a new site
# - Team: goran1310
# - Site name: (choose a unique name or let Netlify generate one)
# - Build command: npm run build
# - Publish directory: build

# Then deploy:
netlify deploy --prod
```

## Option 3: Manual Drag & Drop

### Step 1: Build the App
```powershell
cd 'c:\Users\goran.lovincic\source\repos\Skriv_Glosene_På_Engelsk\vocabulary-trainer-web'
npm run build
```

### Step 2: Deploy
1. Go to https://app.netlify.com/drop
2. Drag the `vocabulary-trainer-web/build` folder to the upload area
3. Wait for deployment to complete

**Note:** This method doesn't support continuous deployment from Git.

## After Deployment

### Custom Domain (Optional)
1. In Netlify dashboard, go to **"Domain settings"**
2. Click **"Add custom domain"**
3. Follow the instructions to configure DNS

### Environment Variables (If needed)
1. In Netlify dashboard, go to **"Site settings"** → **"Environment variables"**
2. Add any required variables

## Features of Your React App

✅ **Add Vocabulary** - Add Norwegian-English word pairs by week
✅ **View Vocabulary** - See all words with filtering by week
✅ **Quiz Mode** - Interactive quiz with:
   - Direction selection (NO→EN or EN→NO)
   - Randomize option
   - Answer hints with underscores
   - Real-time feedback
✅ **Results** - View quiz history and statistics
✅ **Settings** - Set your username
✅ **Persistent Storage** - All data saved in browser localStorage

## Troubleshooting

### Build Fails
- Check that Node.js version is 14+ (`node --version`)
- Clear cache: `npm clean-cache --force`
- Reinstall dependencies: `rm -rf node_modules package-lock.json; npm install`

### App Not Loading
- Check browser console for errors (F12)
- Verify localStorage is enabled in browser
- Clear browser cache and reload

### Data Not Persisting
- localStorage only works in the same browser/device
- Use Export/Import feature (if implemented) to transfer data
- Consider adding a backend database for cross-device sync

## Support
- Netlify Docs: https://docs.netlify.com/
- React Docs: https://react.dev/

---
🎓 Happy Learning Norwegian-English Vocabulary! 📚
