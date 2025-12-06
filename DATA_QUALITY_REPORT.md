# Data Quality Report - vocabulary.csv

## Issues Found

### 1. **CSV Parsing Problems (Critical)**

**Problem**: Commas within words break CSV parsing because commas are the field delimiter.

**Affected Rows**:
- Line 30: `44,fierce,"vill, rasande"` - Has comma in Norwegian translation (quoted)
- Line 34: `39,"Ulik,",ikkje likeverdig Unequal` - Has comma in English word (quoted)
- Line 42: `40,Is required, Trengst, behøvast` - Commas split into wrong columns
- Line 51: `40,Any more Meir, lenger` - Commas create parsing errors
- Line 52: `40,However, Likevel` - Commas create parsing errors
- Line 53: `40,Lift up, Løft opp` - Commas create parsing errors
- Line 54: `40,Catch, Ta i mot` - Commas create parsing errors

**Impact**: These entries will fail to load correctly in quizzes.

**Solutions**:
1. Replace commas with semicolons in translations: `"vill; rasande"`
2. Use quotes properly: `"Is required","Trengst, behøvast"`
3. Remove commas: `"vill rasande"` or `"vill/rasande"`

---

### 2. **Inconsistent Multi-word Entries**

**Problem**: Some entries split multi-word phrases incorrectly.

**Examples**:
- Line 4: `46,stuff,like that sånne ting` - Should be `"stuff like that","sånne ting"`
- Line 8: `46,for,instance for eksempel` - Should be `"for instance","for eksempel"`
- Line 9: `46,started,yelling begynte å skrike` - Should be `"started yelling","begynte å skrike"`
- Line 12: `45,takes,care of tar vare på` - Should be `"takes care of","tar vare på"`
- Line 14: `45,Childcare,agency barnevernet` - Should be `"Childcare agency","barnevernet"`
- Line 17: `45,straight,away med ein gong` - Should be `"straight away","med ein gong"`
- Line 36: `39,Eg,meiner In my opinion` - Should be `"Eg meiner","In my opinion"`
- Line 38: `39,Gå,av med pensjon Retire` - Should be `"Gå av med pensjon","Retire"`

---

### 3. **Inconsistent Capitalization**

**Problem**: Mixed capitalization makes duplicate detection harder.

**Norwegian Words Starting with Capital** (inconsistent):
- Line 32: `Kvinne` (should be lowercase: `kvinne`)
- Line 33: `Utmerkt` (should be lowercase: `utmerkt`)
- Line 34: `Usemje` (should be lowercase: `usemje`)
- Line 35: `Ulik` (should be lowercase: `ulik`)
- Line 36: `Imponerande` (should be lowercase: `imponerande`)
- Line 37: `Eg` (should be lowercase: `eg`)
- Line 38: `Spiss` (should be lowercase: `spiss`)
- Line 39: `Gå` (should be lowercase: `gå`)
- Line 40: `Trene` (should be lowercase: `trene`)
- Line 41: `Helse` (should be lowercase: `helse`)

**English Words Starting with Capital** (some acceptable):
- Line 42-54: Multiple entries (some proper nouns are OK, but common words should be lowercase)

---

### 4. **Language Direction Inconsistency**

**Problem**: Week 39 has columns reversed (Norwegian,English instead of English,Norwegian).

**Affected Rows** (Week 39):
- `Kvinne,Female` - Should be `Female,Kvinne`
- `Utmerkt,Excellent` - Should be `Excellent,Utmerkt`
- `Usemje,Disagreement` - Should be `Disagreement,Usemje`
- etc.

This breaks the quiz system's bidirectional testing.

---

### 5. **Missing or Malformed Entries**

**Potential Issues**:
- Line 34: `"Ulik,",ikkje likeverdig Unequal` - Three parts, unclear structure
- Line 42: `Is required, Trengst, behøvast` - Multiple translations unclear

---

## Recommendations

### Immediate Fixes Required:

1. **Fix CSV Structure**
   - Properly quote all fields containing commas
   - Or replace internal commas with semicolons/slashes
   - Ensure exactly 3 columns per row

2. **Fix Multi-word Phrases**
   - Combine split phrases into single fields
   - Use quotes for phrases with spaces

3. **Fix Week 39 Direction**
   - Swap English/Norwegian columns for all Week 39 entries

4. **Standardize Capitalization**
   - Lowercase for common nouns
   - Capitalize only proper nouns and sentence starts

### Suggested Corrections:

```csv
# Week 46 - Fixed
46,"stuff like that","sånne ting"
46,"for instance","for eksempel"
46,"started yelling","begynte å skrike"

# Week 45 - Fixed
45,"takes care of","tar vare på"
45,"Childcare agency","barnevernet"
45,"straight away","med ein gong"

# Week 44 - Fixed
44,fierce,"vill/rasande"  # Or: "vill; rasande"

# Week 39 - Fixed (swapped columns)
39,female,kvinne
39,excellent,utmerkt
39,disagreement,usemje
39,unequal,"ulik, ikkje likeverdig"
39,impressive,imponerande
39,"in my opinion","eg meiner"
39,striker,spiss
39,retire,"gå av med pensjon"
39,exercise,trene
39,health,helse

# Week 40 - Fixed
40,equipment,utstyr
40,"is required","trengst/behøvast"
40,referee,dommar
40,consider,"reknar som"
40,squads,troppar
40,participate,delta
40,entertain,underhalde
40,audience,publikum
40,competitions,konkurransar
40,tricks,triks
40,"any more","meir/lenger"
40,however,likevel
40,"lift up","løft opp"
40,catch,"ta i mot"
```

---

## Impact on Quiz System

**Current Issues**:
- ❌ CSV parsing failures cause missing words in quizzes
- ❌ Week 39 tests backwards (asking Norwegian→English instead of English→Norwegian)
- ❌ Multi-word phrases broken across columns won't match user answers
- ❌ Inconsistent capitalization may cause matching issues

**After Fixes**:
- ✅ All entries load correctly
- ✅ Bidirectional testing works properly
- ✅ Answer matching improved
- ✅ Better duplicate detection

---

## Automated Fix Available

Run the data cleaning tool to automatically fix these issues:
```powershell
python fix_vocabulary_data.py
```

This will:
1. Create backup: `vocabulary_backup_[timestamp].csv`
2. Fix CSV structure
3. Correct multi-word entries
4. Fix Week 39 direction
5. Standardize capitalization
6. Validate all entries
7. Generate report
