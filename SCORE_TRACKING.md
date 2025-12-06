# Score Tracking System

## Overview
The vocabulary trainer now saves scores in **JSON format** (`data/scores.json`) with detailed statistics and tracking.

## Features

### 📊 Detailed Score Information
Each quiz result includes:
- **Username**: Who took the quiz
- **Date & Time**: When it was completed
- **Quiz Mode**: Mode A or Mode B
- **Weeks Tested**: Which weeks were covered
- **Direction**: NO→EN or EN→NO
- **Questions**: Total and correct answers
- **Score Percentage**: Calculated automatically
- **Time Taken**: How long the quiz took (in seconds)

### 📈 User Statistics
For each user, the system tracks:
- **Total Quizzes**: Number of quizzes completed
- **Average Score**: Overall performance percentage
- **Best Score**: Highest score achieved
- **Total Questions**: All questions answered
- **Total Correct**: All correct answers
- **First/Last Quiz**: When started and last practiced

### 💾 Data Storage

#### JSON File Structure (`data/scores.json`)
```json
{
  "users": {
    "Student": {
      "first_quiz": "2025-12-06T10:30:00",
      "total_quizzes": 5,
      "total_questions": 50,
      "total_correct": 42,
      "best_score": 95.0,
      "average_score": 84.0,
      "last_quiz": "2025-12-06T11:15:00",
      "quizzes": [1, 2, 3, 4, 5]
    }
  },
  "all_scores": [
    {
      "id": 1,
      "username": "Student",
      "date": "2025-12-06",
      "time": "10:30:15",
      "timestamp": "2025-12-06T10:30:15",
      "mode": "Mode A (Random)",
      "weeks": "Week 46",
      "direction": "NO→EN",
      "total_questions": 10,
      "correct_answers": 8,
      "wrong_answers": 2,
      "score_percentage": 80.0,
      "time_taken_seconds": 125
    }
  ]
}
```

## Usage

### In GUI Application

#### View Your Scores
1. Click **📊 My Scores** from main menu
2. See your statistics:
   - Total quizzes taken
   - Average score
   - Best score
   - Total questions answered
3. Browse last 10 quiz results with:
   - Date
   - Weeks tested
   - Direction (NO→EN or EN→NO)
   - Score and percentage
   - Time taken

#### Export Your Data
1. Go to **📊 My Scores**
2. Click **💾 Export Data** button
3. Your data will be saved to:
   ```
   data/export_YourName_YYYYMMDD_HHMMSS.json
   ```

### Programmatic Access

```python
from storage import ScoreStorageJSON

# Initialize
score_storage = ScoreStorageJSON()

# Save a score
score_storage.save_score(
    username="Student",
    mode="Mode A",
    weeks="Week 46",
    total_questions=10,
    correct_answers=8,
    time_taken_seconds=120,
    direction="NO→EN"
)

# Get user scores
scores = score_storage.get_user_scores("Student")

# Get user statistics
stats = score_storage.get_user_stats("Student")
print(f"Average: {stats['average_score']}%")
print(f"Best: {stats['best_score']}%")

# Get leaderboard
top_users = score_storage.get_leaderboard(limit=10)

# Export user data
export_path = score_storage.export_user_data("Student")
```

## Benefits

### ✅ Compared to CSV Storage
- **Richer Data**: Direction, time taken, timestamps
- **User Statistics**: Automatic calculation of averages, bests
- **Structured**: Easy to query and analyze
- **Exportable**: Each user can export their own data
- **Backwards Compatible**: Still saves to CSV for legacy support

### 📱 Use Cases
- **Track Progress**: See improvement over time
- **Identify Weak Areas**: Which directions need practice
- **Set Goals**: Aim to beat your best score
- **Export for Portfolio**: Save your learning journey
- **Multiple Users**: Each user has separate statistics

## File Locations

- **JSON Scores**: `data/scores.json`
- **CSV Results** (legacy): `data/results.csv`
- **Exported Data**: `data/export_USERNAME_TIMESTAMP.json`

## Backup & Recovery

The JSON file is automatically created if missing. To backup:
```powershell
Copy-Item data/scores.json data/scores_backup.json
```

To restore from backup:
```powershell
Copy-Item data/scores_backup.json data/scores.json
```

## Future Enhancements

Possible additions:
- 📊 Charts and graphs of progress
- 🏆 Achievements and badges
- 📅 Weekly/monthly reports
- 🎯 Goal setting and tracking
- 👥 Multi-user leaderboards
