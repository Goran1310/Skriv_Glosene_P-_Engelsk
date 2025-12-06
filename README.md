# Skriv Glosene På Engelsk 🇳🇴 ↔️ 🇬🇧

**Norwegian/English Vocabulary Training Application**

A Python-based interactive vocabulary training system for learning Norwegian and English word pairs. Perfect for weekly vocabulary practice with quiz modes and historical progress tracking.

---

## ✨ Features

- **📝 Weekly Vocabulary Management**: Add and organize vocabulary in weekly sets (any number of words)
- **🔍 Duplicate Detection**: Automatic checking for duplicate vocabulary pairs
  - Detects exact matches (same English and Norwegian)
  - Warns about English words with different translations
  - Warns about Norwegian words with different English translations
- **🎯 Two Quiz Modes**:
  - **Mode A**: Practice a single week (sequential or randomized)
  - **Mode B**: Practice multiple recent weeks combined
- **🔄 Bidirectional Testing**: Questions randomly test both EN→NO and NO→EN
- **📊 Historical Results**: Track all quiz attempts with date, time, and scores
- **👤 Multi-user Support**: Track results per username
- **💾 CSV-based Storage**: Simple, portable data storage

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Installation

1. Clone or download this repository:
   ```bash
   cd Skriv_Glosene_På_Engelsk
   ```

2. Run the application:
   ```bash
   python main.py
   ```

---

## 📖 How to Use

### 1. **Add Vocabulary**

Choose option `1` from the main menu to add a new week's vocabulary.

**Interactive Method** (one by one):
```
1. Enter pair (EN, NO): greedy, grådig
2. Enter pair (EN, NO): above all, meir enn noko anna
...
```

**Bulk Paste Method** (all at once):
```
greedy grådig
above all meir enn noko anna
selfish egoistisk
spirits ånder
regretful angrande
ashamed skamfull
positively til og med, sanneleg
grateful takknemleg
various forskjellige
rush of happiness lykkerus
```

### 2. **Take a Quiz**

#### Mode A: Single Week Practice
- Select a specific week
- Choose randomized or sequential order
- Answer all 10 questions
- Get immediate feedback

#### Mode B: Multi-Week Practice
- Choose how many recent weeks to include
- Questions are randomized from all selected weeks
- Test your cumulative knowledge

### 3. **View Results**

- View all quiz results (option `6`)
- View your personal results (option `7`)
- Results include: date, time, mode, weeks tested, score

---

## 📂 Project Structure

```
Skriv_Glosene_På_Engelsk/
│
├── main.py              # Application entry point & menu system
├── storage.py           # CSV storage for vocabulary & results
├── vocabulary.py        # Vocabulary management
├── quiz.py              # Quiz modes A & B
├── README.md            # This file
│
└── data/
    ├── vocabulary.csv   # Vocabulary storage (auto-created)
    └── results.csv      # Quiz results history (auto-created)
```

---

## 💡 Example Vocabulary (Week 1)

| English | Norwegian |
|---------|-----------|
| greedy | grådig |
| above all | meir enn noko anna |
| selfish | egoistisk |
| spirits | ånder |
| regretful | angrande |
| ashamed | skamfull |
| positively | til og med, sanneleg |
| grateful | takknemleg |
| various | forskjellige |
| rush of happiness | lykkerus |

---

## 🎮 Menu Options

```
1. Add New Weekly Vocabulary (10 words)
2. View Vocabulary by Week
3. View All Available Weeks
4. Take Quiz - Mode A (Single Week)
5. Take Quiz - Mode B (Multiple Weeks)
6. View Quiz Results
7. View My Results
8. Change Username
0. Exit
```

---

## 🔧 Technical Details

### Data Storage

**vocabulary.csv format:**
```csv
week,english,norwegian
1,greedy,grådig
1,selfish,egoistisk
...
```

**results.csv format:**
```csv
username,date,time,mode,weeks,total_questions,correct_answers,score_percentage
John,2025-12-06,14:30:15,Mode A (Random),Week 1,10,8,80.0
...
```

### Answer Validation

The quiz accepts answers that:
- Match exactly (case-insensitive)
- Contain all required words for multi-word phrases
- This allows some flexibility while maintaining accuracy

---

## 🎯 Use Cases

- **Students**: Weekly vocabulary homework practice
- **Language Learners**: Self-paced Norwegian/English learning
- **Teachers**: Track student progress over time
- **Families**: Multi-user learning environment

---

## 🚀 Future Enhancement Ideas

- [ ] Spaced repetition algorithm
- [ ] Difficulty levels based on past performance
- [ ] Web interface (Flask/FastAPI)
- [ ] Mobile app version
- [ ] Audio pronunciation support
- [ ] Export results to PDF/Excel
- [ ] Synonyms and alternative answers
- [ ] Timed quiz mode
- [ ] Leaderboard system

---

## 📝 License

This project is open source and available for educational purposes.

---

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to fork and submit pull requests.

---

## 📧 Support

For questions or issues, please create an issue in the repository.

---

**Lykke til med norsktreningen! (Good luck with your Norwegian practice!)** 🎓
