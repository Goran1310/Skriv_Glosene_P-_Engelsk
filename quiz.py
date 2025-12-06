"""
Quiz module for vocabulary testing.
Implements Mode A (single week) and Mode B (multiple weeks) quiz modes.
"""

import random
from typing import List, Dict
from storage import VocabularyStorage, ResultsStorage


class QuizMode:
    """Base class for quiz modes."""
    
    def __init__(self, vocab_storage: VocabularyStorage, results_storage: ResultsStorage):
        self.vocab_storage = vocab_storage
        self.results_storage = results_storage
    
    def _normalize_answer(self, answer: str) -> str:
        """Normalize answer for comparison (lowercase, stripped)."""
        return answer.strip().lower()
    
    def _check_answer(self, user_answer: str, correct_answer: str) -> bool:
        """
        Check if user's answer is correct.
        Allows for minor variations in spelling.
        """
        user_norm = self._normalize_answer(user_answer)
        correct_norm = self._normalize_answer(correct_answer)
        
        # Exact match
        if user_norm == correct_norm:
            return True
        
        # Check if answer contains the correct word (for multi-word phrases)
        # This is lenient but useful for phrases
        if ' ' in correct_norm:
            correct_words = set(correct_norm.split())
            user_words = set(user_norm.split())
            # If all correct words are in user's answer
            if correct_words.issubset(user_words):
                return True
        
        return False
    
    def _run_quiz_questions(self, questions: List[Dict], mode_name: str, 
                          weeks_info: str, username: str):
        """
        Run through quiz questions and save results.
        
        Args:
            questions: List of question dictionaries
            mode_name: Name of the quiz mode
            weeks_info: String describing which weeks were tested
            username: Username taking the quiz
        """
        total = len(questions)
        correct = 0
        
        print(f"\n{'='*60}")
        print(f"Starting Quiz: {mode_name}")
        print(f"Total Questions: {total}")
        print(f"{'='*60}\n")
        
        for i, q in enumerate(questions, 1):
            print(f"Question {i}/{total}")
            print(f"Translate: {q['question']}")
            
            user_answer = input("Your answer: ").strip()
            
            if self._check_answer(user_answer, q['correct_answer']):
                print("✓ Correct!\n")
                correct += 1
            else:
                print(f"✗ Incorrect. Correct answer: {q['correct_answer']}\n")
        
        # Display results
        percentage = (correct / total * 100) if total > 0 else 0
        print(f"\n{'='*60}")
        print(f"Quiz Complete!")
        print(f"Score: {correct}/{total} ({percentage:.1f}%)")
        print(f"{'='*60}\n")
        
        # Save results
        self.results_storage.save_result(
            username=username,
            mode=mode_name,
            weeks=weeks_info,
            total_questions=total,
            correct_answers=correct
        )
        print("✓ Results saved to history.")


class ModeA(QuizMode):
    """
    Mode A: Practice same ten words from a specific week.
    Can run in order or random loop.
    """
    
    def run(self, week: int, username: str, randomize: bool = True):
        """
        Run Mode A quiz.
        
        Args:
            week: Week number to practice
            username: Username taking the quiz
            randomize: If True, randomize order; if False, keep original order
        """
        vocab = self.vocab_storage.get_vocabulary_by_week(week)
        
        if not vocab:
            print(f"\nNo vocabulary found for Week {week}.")
            return
        
        print(f"\nQuiz will include {len(vocab)} words from Week {week}.")
        
        # Create questions (randomly choose direction for each)
        questions = []
        for item in vocab:
            # Randomly choose EN→NO or NO→EN
            if random.choice([True, False]):
                questions.append({
                    'question': item['english'],
                    'correct_answer': item['norwegian'],
                    'direction': 'EN→NO'
                })
            else:
                questions.append({
                    'question': item['norwegian'],
                    'correct_answer': item['english'],
                    'direction': 'NO→EN'
                })
        
        # Randomize order if requested
        if randomize:
            random.shuffle(questions)
        
        mode_name = f"Mode A ({'Random' if randomize else 'Sequential'})"
        weeks_info = f"Week {week}"
        
        self._run_quiz_questions(questions, mode_name, weeks_info, username)


class ModeB(QuizMode):
    """
    Mode B: Practice last X weeks from vocabulary database.
    """
    
    def run(self, num_weeks: int, username: str):
        """
        Run Mode B quiz.
        
        Args:
            num_weeks: Number of recent weeks to include
            username: Username taking the quiz
        """
        all_weeks = self.vocab_storage.get_all_weeks()
        
        if not all_weeks:
            print("\nNo vocabulary data available.")
            return
        
        # Get the last X weeks
        weeks_to_practice = all_weeks[-num_weeks:] if num_weeks < len(all_weeks) else all_weeks
        
        print(f"\nPracticing weeks: {', '.join(map(str, weeks_to_practice))}")
        
        # Get all vocabulary for these weeks
        vocab = self.vocab_storage.get_vocabulary_by_weeks(weeks_to_practice)
        
        if not vocab:
            print("\nNo vocabulary found for selected weeks.")
            return
        
        # Create questions (randomly choose direction for each)
        questions = []
        for item in vocab:
            # Randomly choose EN→NO or NO→EN
            if random.choice([True, False]):
                questions.append({
                    'question': item['english'],
                    'correct_answer': item['norwegian'],
                    'direction': 'EN→NO'
                })
            else:
                questions.append({
                    'question': item['norwegian'],
                    'correct_answer': item['english'],
                    'direction': 'NO→EN'
                })
        
        # Always randomize in Mode B
        random.shuffle(questions)
        
        mode_name = "Mode B (Multi-week)"
        weeks_info = f"Weeks {min(weeks_to_practice)}-{max(weeks_to_practice)}"
        
        self._run_quiz_questions(questions, mode_name, weeks_info, username)


class QuizManager:
    """High-level quiz management."""
    
    def __init__(self, vocab_storage: VocabularyStorage, results_storage: ResultsStorage):
        self.mode_a = ModeA(vocab_storage, results_storage)
        self.mode_b = ModeB(vocab_storage, results_storage)
    
    def run_mode_a(self, week: int, username: str, randomize: bool = True):
        """Run Mode A quiz."""
        self.mode_a.run(week, username, randomize)
    
    def run_mode_b(self, num_weeks: int, username: str):
        """Run Mode B quiz."""
        self.mode_b.run(num_weeks, username)
