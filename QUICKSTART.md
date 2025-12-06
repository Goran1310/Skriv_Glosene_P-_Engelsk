# Quick Start Guide

## Running the Application

### Windows PowerShell
```powershell
cd "c:\Users\goran.lovincic\source\repos\Skriv_Glosene_På_Engelsk"
python main.py
```

### Alternative: Using Python directly
```powershell
python -m main
```

---

## First-Time Setup

1. **Run the application**:
   ```powershell
   python main.py
   ```

2. **Add your first vocabulary** (Option 1):
   - Choose option `1` from the menu
   - Enter week number: `1`
   - Enter 10 vocabulary pairs

3. **Or load example data**:
   ```powershell
   python example_data_loader.py
   ```

4. **Take your first quiz** (Option 4 or 5):
   - Enter your name
   - Choose Mode A or B
   - Start practicing!

---

## Quick Command Reference

### Add Example Data
```powershell
python example_data_loader.py
```

### Run Main Application
```powershell
python main.py
```

### View Data Files
```powershell
# View vocabulary
Get-Content data\vocabulary.csv

# View results
Get-Content data\results.csv
```

---

## Common Tasks

### Add Week 1 Vocabulary (Interactive)
1. Run: `python main.py`
2. Choose: `1` (Add New Weekly Vocabulary)
3. Enter week: `1`
4. Choose input method: `1` (Interactive)
5. Enter each pair when prompted

### Take a Quick Quiz
1. Run: `python main.py`
2. Choose: `4` (Mode A)
3. Enter week: `1`
4. Answer: `y` (Randomize)
5. Type your answers!

### View Your Progress
1. Run: `python main.py`
2. Choose: `7` (View My Results)
3. Enter your name

---

## Sample Session

```
$ python main.py

============================================================
  Welcome to Skriv Glosene På Engelsk!
  Norwegian/English Vocabulary Training System
============================================================

============================================================
  SKRIV GLOSENE PÅ ENGELSK - Vocabulary Training
============================================================
1. Add New Weekly Vocabulary (10 words)
2. View Vocabulary by Week
3. View All Available Weeks
4. Take Quiz - Mode A (Single Week)
5. Take Quiz - Mode B (Multiple Weeks)
6. View Quiz Results
7. View My Results
8. Change Username
0. Exit
============================================================

Enter your choice: 4

Enter your name: John

Available weeks: 1, 2
Enter week number to practice: 1
Randomize order? (y/n, default=y): y

============================================================
Starting Quiz: Mode A (Random)
Total Questions: 10
============================================================

Question 1/10
Translate: grateful
Your answer: takknemleg
✓ Correct!

...
```

---

## Tips

- **Use Tab**: Some terminals support tab completion
- **Ctrl+C**: Exit anytime safely
- **Case doesn't matter**: "Grådig" = "grådig"
- **Spaces count**: Be careful with multi-word phrases
- **Weekly practice**: Add vocabulary every week for best results

---

Lykke til! 🎓
