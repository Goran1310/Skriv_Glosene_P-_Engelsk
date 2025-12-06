# Manual Data Corrections Needed

The automated cleaner fixed many issues, but some entries still need manual review:

## Week 46 - Multi-word Phrases Split Incorrectly

**Current Issues:**
```csv
46,stuff,like that sånne ting        → Should be: "stuff like that","sånne ting"
46,for,instance for eksempel          → Should be: "for instance","for eksempel"
46,started,yelling begynte å skrike   → Should be: "started yelling","begynte å skrike"
```

**How to Fix:**
These need proper multi-word phrase handling. The English and Norwegian parts are split incorrectly.

**Corrected:**
```csv
46,"stuff like that","sånne ting"
46,"for instance","for eksempel"  
46,"started yelling","begynte å skrike"
```

---

## Week 45 - Similar Issues

**Current:**
```csv
45,takes,care of tar vare på         → Should be: "takes care of","tar vare på"
45,childcare,agency barnevernet      → Should be: "childcare agency","barnevernet"
45,straight,away med ein gong        → Should be: "straight away","med ein gong"
```

**Corrected:**
```csv
45,"takes care of","tar vare på"
45,"childcare agency","barnevernet"
45,"straight away","med ein gong"
```

---

## Week 39 - Still Has Issues

**Current (after column swap):**
```csv
39,ikkje likeverdig Unequal,ulik      → Unclear what this should be
39,meiner In my opinion,eg            → Should be: "in my opinion","eg meiner"
39,av med pensjon Retire,gå           → Should be: "retire","gå av med pensjon"
```

**Suggested Corrections:**
```csv
39,unequal,"ulik; ikkje likeverdig"
39,"in my opinion","eg meiner"
39,retire,"gå av med pensjon"
```

---

## Week 40 - Remaining Issues

**Current:**
```csv
40,is,required Trengst; behøvast      → Should be: "is required","trengst; behøvast"
40,consider,Reknar som                → Should be: "consider","reknar som"
```

**Corrected:**
```csv
40,"is required","trengst; behøvast"
40,consider,"reknar som"
```

---

## How to Apply Manual Corrections

### Option 1: Edit CSV Directly
1. Open `data/vocabulary.csv` in a text editor (NOT Excel - it breaks CSV)
2. Use the corrected lines above
3. Save with UTF-8 encoding

### Option 2: Delete and Re-add
1. Delete problematic weeks from CSV
2. Use the app to re-add them properly:
   ```
   python main.py
   → Choose option 1 (Add vocabulary)
   → Enter week number
   → Add words correctly with proper formatting
   ```

### Option 3: Use Bulk Import with Proper Format
Create a text file `week46_corrected.txt`:
```
stuff like that	sånne ting
for instance	for eksempel
started yelling	begynte å skrike
```

Then paste into bulk import mode (using TAB between columns).

---

## Prevention: Best Practices

### When Adding Multi-word Phrases:

**✅ DO:**
- Use TAB to separate English from Norwegian
- Use 2+ spaces to separate if no tab available
- Quote phrases in CSV: `"phrase here","setning her"`

**❌ DON'T:**
- Use single space if phrase contains spaces
- Use commas within translations (use semicolon instead)
- Mix languages in same column

### Examples:

**Good Input (TAB separated):**
```
for instance<TAB>for eksempel
in my opinion<TAB>eg meiner
```

**Good Input (multiple spaces):**
```
for instance    for eksempel
in my opinion   eg meiner
```

**Bad Input (single space):**
```
for instance for eksempel  ← WRONG! Will parse as 3 parts
```

---

## Quick Fix Script

Run this to manually correct the most problematic entries:

```python
python manual_corrections.py
```

This will:
1. Fix all multi-word phrase splits
2. Properly quote CSV entries
3. Create another backup
4. Validate all entries
