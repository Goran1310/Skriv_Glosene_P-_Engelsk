# Quick Reference: Fixed Issues & Prevention

## ✅ What Was Fixed

### Issue 1: Commas Breaking CSV
**Before**: `fierce,"vill, rasande"` ← Quoted commas cause parsing issues  
**After**: `fierce,vill; rasande` ← Semicolons work perfectly  
**Prevention**: The app now auto-converts commas to semicolons with a warning

### Issue 2: Multi-word Phrases Split Wrong
**Before**: `46,for,instance for eksempel` ← 3 columns instead of 2!  
**After**: `46,for instance,for eksempel` ← Correct 2 columns  
**Prevention**: Use TAB or multiple spaces when pasting

### Issue 3: Reversed Columns (Week 39)
**Before**: `39,Kvinne,Female` ← Norwegian in English column!  
**After**: `39,female,kvinne` ← Correct direction + lowercase  
**Prevention**: Always use format: `english,norwegian`

## 🛡️ How to Prevent Issues When Adding Words

### Interactive Mode (Option 1)
```
Format: english, norwegian
Example: happy, glad ✅
Example: for instance, for eksempel ✅
```
The comma separator works fine here!

### Bulk Paste Mode (Option 2)

**✅ CORRECT - Use TAB:**
```
happy<TAB>glad
for instance<TAB>for eksempel
is required<TAB>trengst; behøvast
```

**✅ CORRECT - Use Multiple Spaces:**
```
happy    glad
for instance    for eksempel
is required     trengst; behøvast
```

**❌ WRONG - Single Space with Multi-word:**
```
for instance for eksempel  ← Will parse as 3 parts!
```

## 🎯 Golden Rules

1. **Interactive input**: Use `, ` (comma-space) separator
2. **Bulk paste**: Use TAB or 2+ spaces
3. **Avoid commas in translations**: Use `;` or `/` instead
4. **Lowercase common words**: `happy, glad` not `Happy, Glad`
5. **Consistent direction**: Always `english,norwegian`

## 🧰 Tools Available

```powershell
# Clean existing data
python fix_vocabulary_data.py

# Apply manual corrections
python manual_corrections.py

# Test duplicate detection
python test_duplicates.py

# Run the app
python main.py
```

## 📖 Example Session

```
$ python main.py

Choose: 1 (Add vocabulary)
Week: 50
How many: 5
Method: 2 (Bulk paste)

Paste lines:
happy	glad
sad	trist
angry	sint
tired	trøtt
hungry	sulten
<press Enter on empty line>

✓ Successfully added 5 vocabulary pairs!
```

---

**Need help?** Check:
- `CLEANING_SUMMARY.md` - Full cleaning report
- `DATA_QUALITY_REPORT.md` - Detailed analysis
- `MANUAL_CORRECTIONS_NEEDED.md` - Correction guide
