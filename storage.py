"""
Storage module for vocabulary and quiz results.
Handles CSV-based persistence for vocabulary lists and historical results.
Also provides JSON-based storage for detailed score tracking.
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple


class VocabularyStorage:
    """Handles storage operations for vocabulary lists."""
    
    def __init__(self, vocab_file: str = "data/vocabulary.csv"):
        self.vocab_file = vocab_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create vocabulary file with headers if it doesn't exist."""
        if not os.path.exists(self.vocab_file):
            os.makedirs(os.path.dirname(self.vocab_file), exist_ok=True)
            with open(self.vocab_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['week', 'english', 'norwegian'])
    
    def check_duplicate(self, english: str, norwegian: str, week: int = None) -> Dict:
        """
        Check if a vocabulary pair already exists.
        
        Args:
            english: English word/phrase
            norwegian: Norwegian word/phrase
            week: Optional week number to check within specific week only
            
        Returns:
            Dict with 'exists' (bool), 'week' (int or None), 'match_type' (str)
        """
        if not os.path.exists(self.vocab_file):
            return {'exists': False, 'week': None, 'match_type': None}
        
        english_norm = english.strip().lower()
        norwegian_norm = norwegian.strip().lower()
        
        with open(self.vocab_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_week = int(row['week'])
                row_en = row['english'].strip().lower()
                row_no = row['norwegian'].strip().lower()
                
                # Check if we should filter by week
                if week is not None and row_week != week:
                    continue
                
                # Exact match
                if row_en == english_norm and row_no == norwegian_norm:
                    return {'exists': True, 'week': row_week, 'match_type': 'exact'}
                
                # English word exists with different translation
                if row_en == english_norm:
                    return {'exists': True, 'week': row_week, 'match_type': 'english_only'}
                
                # Norwegian word exists with different English
                if row_no == norwegian_norm:
                    return {'exists': True, 'week': row_week, 'match_type': 'norwegian_only'}
        
        return {'exists': False, 'week': None, 'match_type': None}
    
    def add_weekly_vocabulary(self, week: int, vocab_pairs: List[Tuple[str, str]], 
                            skip_duplicates: bool = True) -> Dict:
        """
        Add a new week's vocabulary to the storage.
        
        Args:
            week: Week number
            vocab_pairs: List of (english, norwegian) tuples
            skip_duplicates: If True, skip duplicate pairs and report them
            
        Returns:
            Dict with 'added' (int), 'skipped' (int), 'duplicates' (list)
        """
        added = 0
        skipped = 0
        duplicates = []
        
        with open(self.vocab_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for english, norwegian in vocab_pairs:
                if skip_duplicates:
                    dup_check = self.check_duplicate(english, norwegian)
                    if dup_check['exists']:
                        skipped += 1
                        duplicates.append({
                            'english': english,
                            'norwegian': norwegian,
                            'existing_week': dup_check['week'],
                            'match_type': dup_check['match_type']
                        })
                        continue
                
                writer.writerow([week, english.strip(), norwegian.strip()])
                added += 1
        
        return {'added': added, 'skipped': skipped, 'duplicates': duplicates}
    
    def get_vocabulary_by_week(self, week: int) -> List[Dict[str, str]]:
        """
        Get vocabulary for a specific week.
        
        Args:
            week: Week number
            
        Returns:
            List of dictionaries with 'english' and 'norwegian' keys
        """
        vocab = []
        if not os.path.exists(self.vocab_file):
            return vocab
            
        with open(self.vocab_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['week']) == week:
                    vocab.append({
                        'english': row['english'],
                        'norwegian': row['norwegian']
                    })
        return vocab
    
    def get_vocabulary_by_weeks(self, weeks: List[int]) -> List[Dict[str, str]]:
        """
        Get vocabulary for multiple weeks.
        
        Args:
            weeks: List of week numbers
            
        Returns:
            List of dictionaries with 'english' and 'norwegian' keys
        """
        vocab = []
        if not os.path.exists(self.vocab_file):
            return vocab
            
        with open(self.vocab_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['week']) in weeks:
                    vocab.append({
                        'english': row['english'],
                        'norwegian': row['norwegian']
                    })
        return vocab
    
    def get_all_weeks(self) -> List[int]:
        """Get a sorted list of all available week numbers."""
        weeks = set()
        if not os.path.exists(self.vocab_file):
            return []
            
        with open(self.vocab_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                weeks.add(int(row['week']))
        return sorted(weeks)


class ResultsStorage:
    """Handles storage operations for quiz results."""
    
    def __init__(self, results_file: str = "data/results.csv"):
        self.results_file = results_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create results file with headers if it doesn't exist."""
        if not os.path.exists(self.results_file):
            os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
            with open(self.results_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'date', 'time', 'mode', 'weeks', 
                               'total_questions', 'correct_answers', 'score_percentage'])
    
    def save_result(self, username: str, mode: str, weeks: str, 
                   total_questions: int, correct_answers: int):
        """
        Save a quiz result.
        
        Args:
            username: Name of the user
            mode: Quiz mode (A or B)
            weeks: Week identifier (e.g., "Week 1" or "Weeks 1-3")
            total_questions: Total number of questions
            correct_answers: Number of correct answers
        """
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')
        score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        with open(self.results_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([username, date_str, time_str, mode, weeks, 
                           total_questions, correct_answers, f"{score_percentage:.1f}"])
    
    def get_all_results(self) -> List[Dict[str, str]]:
        """Get all quiz results."""
        results = []
        if not os.path.exists(self.results_file):
            return results
            
        with open(self.results_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
        return results
    
    def get_results_by_user(self, username: str) -> List[Dict[str, str]]:
        """Get results for a specific user."""
        results = []
        if not os.path.exists(self.results_file):
            return results
            
        with open(self.results_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'].lower() == username.lower():
                    results.append(row)
        return results
    
    def display_results(self, results: List[Dict[str, str]]):
        """Display results in a formatted table."""
        if not results:
            print("\nNo results found.")
            return
        
        print("\n" + "="*100)
        print(f"{'Username':<15} {'Date':<12} {'Time':<10} {'Mode':<6} {'Weeks':<15} "
              f"{'Questions':<10} {'Correct':<8} {'Score':<8}")
        print("="*100)
        
        for result in results:
            print(f"{result['username']:<15} {result['date']:<12} {result['time']:<10} "
                  f"{result['mode']:<6} {result['weeks']:<15} "
                  f"{result['total_questions']:<10} {result['correct_answers']:<8} "
                  f"{result['score_percentage']:<8}%")
        
        print("="*100)


class ScoreStorageJSON:
    """Handles JSON-based storage for detailed user scores and statistics."""
    
    def __init__(self, scores_file: str = "data/scores.json"):
        self.scores_file = scores_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create scores JSON file if it doesn't exist."""
        if not os.path.exists(self.scores_file):
            os.makedirs(os.path.dirname(self.scores_file), exist_ok=True)
            with open(self.scores_file, 'w', encoding='utf-8') as f:
                json.dump({"users": {}, "all_scores": []}, f, indent=2)
    
    def _load_data(self) -> Dict:
        """Load all score data from JSON file."""
        try:
            with open(self.scores_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"users": {}, "all_scores": []}
    
    def _save_data(self, data: Dict):
        """Save score data to JSON file."""
        with open(self.scores_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def save_score(self, username: str, mode: str, weeks: str, 
                   total_questions: int, correct_answers: int,
                   time_taken_seconds: int = None, 
                   direction: str = None) -> Dict:
        """
        Save a detailed quiz score to JSON.
        
        Args:
            username: Name of the user
            mode: Quiz mode (e.g., "Mode A", "Mode B")
            weeks: Week identifier
            total_questions: Total number of questions
            correct_answers: Number of correct answers
            time_taken_seconds: Optional time taken in seconds
            direction: Optional quiz direction (NO→EN or EN→NO)
            
        Returns:
            Dict with the saved score entry
        """
        data = self._load_data()
        
        now = datetime.now()
        score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        score_entry = {
            "id": len(data["all_scores"]) + 1,
            "username": username,
            "date": now.strftime('%Y-%m-%d'),
            "time": now.strftime('%H:%M:%S'),
            "timestamp": now.isoformat(),
            "mode": mode,
            "weeks": weeks,
            "direction": direction or "mixed",
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "wrong_answers": total_questions - correct_answers,
            "score_percentage": round(score_percentage, 1),
            "time_taken_seconds": time_taken_seconds
        }
        
        # Add to all scores
        data["all_scores"].append(score_entry)
        
        # Update user statistics
        if username not in data["users"]:
            data["users"][username] = {
                "first_quiz": now.isoformat(),
                "total_quizzes": 0,
                "total_questions": 0,
                "total_correct": 0,
                "best_score": 0,
                "average_score": 0,
                "last_quiz": None,
                "quizzes": []
            }
        
        user_data = data["users"][username]
        user_data["total_quizzes"] += 1
        user_data["total_questions"] += total_questions
        user_data["total_correct"] += correct_answers
        user_data["best_score"] = max(user_data["best_score"], score_percentage)
        user_data["average_score"] = round(
            (user_data["total_correct"] / user_data["total_questions"] * 100), 1
        )
        user_data["last_quiz"] = now.isoformat()
        user_data["quizzes"].append(score_entry["id"])
        
        self._save_data(data)
        return score_entry
    
    def get_user_scores(self, username: str) -> List[Dict]:
        """Get all scores for a specific user."""
        data = self._load_data()
        return [
            score for score in data["all_scores"] 
            if score["username"].lower() == username.lower()
        ]
    
    def get_user_stats(self, username: str) -> Dict:
        """Get statistics for a specific user."""
        data = self._load_data()
        return data["users"].get(username, None)
    
    def get_all_users(self) -> List[str]:
        """Get list of all users."""
        data = self._load_data()
        return list(data["users"].keys())
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """
        Get top users by average score.
        
        Args:
            limit: Maximum number of users to return
            
        Returns:
            List of user data sorted by average score
        """
        data = self._load_data()
        leaderboard = [
            {
                "username": username,
                "average_score": user_data["average_score"],
                "total_quizzes": user_data["total_quizzes"],
                "best_score": user_data["best_score"]
            }
            for username, user_data in data["users"].items()
        ]
        return sorted(leaderboard, key=lambda x: x["average_score"], reverse=True)[:limit]
    
    def get_recent_scores(self, limit: int = 10) -> List[Dict]:
        """Get most recent scores across all users."""
        data = self._load_data()
        return data["all_scores"][-limit:][::-1]  # Last N scores, reversed
    
    def export_user_data(self, username: str, export_file: str = None) -> str:
        """
        Export all data for a specific user to JSON file.
        
        Args:
            username: Name of the user
            export_file: Optional output file path
            
        Returns:
            Path to the exported file
        """
        if export_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_file = f"data/export_{username}_{timestamp}.json"
        
        data = self._load_data()
        user_stats = data["users"].get(username)
        user_scores = self.get_user_scores(username)
        
        export_data = {
            "username": username,
            "statistics": user_stats,
            "scores": user_scores,
            "exported_at": datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(export_file), exist_ok=True)
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return export_file
