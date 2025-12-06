"""
Vocabulary module for managing weekly word lists.
Handles input and retrieval of vocabulary data.
"""

from typing import List, Tuple
from storage import VocabularyStorage


class VocabularyManager:
    """Manages vocabulary input and retrieval operations."""
    
    def __init__(self, storage: VocabularyStorage):
        self.storage = storage
    
    def input_weekly_vocabulary(self, week: int, num_words: int = 10) -> bool:
        """
        Interactive input for a new week's vocabulary.
        
        Args:
            week: Week number
            num_words: Number of vocabulary pairs to add (default: 10)
            
        Returns:
            True if vocabulary was successfully added, False otherwise
        """
        print(f"\n=== Adding Vocabulary for Week {week} ===")
        print(f"Enter up to {num_words} vocabulary pairs (English → Norwegian)")
        print("Format: english word/phrase, norwegian translation")
        print("Example: greedy, grådig")
        print("Type 'done' to finish early")
        print("-" * 50)
        
        vocab_pairs = []
        
        for i in range(1, num_words + 1):
            while True:
                try:
                    user_input = input(f"{i}. Enter pair (EN, NO): ").strip()
                    
                    if user_input.lower() == 'done':
                        if vocab_pairs:
                            print(f"\nFinishing with {len(vocab_pairs)} pairs.")
                            self.storage.add_weekly_vocabulary(week, vocab_pairs)
                            print(f"✓ Successfully added {len(vocab_pairs)} vocabulary pairs for Week {week}!")
                            return True
                        else:
                            print("   No pairs entered yet. Continue or press Ctrl+C to cancel.")
                            continue
                    
                    if not user_input:
                        print("   Empty input. Please try again or type 'done' to finish.")
                        continue
                    
                    # Split by comma
                    parts = [part.strip() for part in user_input.split(',')]
                    
                    if len(parts) != 2:
                        print("   Invalid format. Use: english, norwegian")
                        continue
                    
                    english, norwegian = parts
                    
                    if not english or not norwegian:
                        print("   Both English and Norwegian words are required.")
                        continue
                    
                    # Check for duplicates
                    dup_check = self.storage.check_duplicate(english, norwegian)
                    if dup_check['exists']:
                        if dup_check['match_type'] == 'exact':
                            print(f"   ⚠ Duplicate: This exact pair exists in Week {dup_check['week']}")
                            retry = input("   Add anyway? (y/n): ").strip().lower()
                            if retry != 'y':
                                continue
                        elif dup_check['match_type'] == 'english_only':
                            print(f"   ⚠ '{english}' already exists in Week {dup_check['week']} with different translation")
                            retry = input("   Add anyway? (y/n): ").strip().lower()
                            if retry != 'y':
                                continue
                        elif dup_check['match_type'] == 'norwegian_only':
                            print(f"   ⚠ '{norwegian}' already exists in Week {dup_check['week']} with different English")
                            retry = input("   Add anyway? (y/n): ").strip().lower()
                            if retry != 'y':
                                continue
                    
                    vocab_pairs.append((english, norwegian))
                    break
                    
                except KeyboardInterrupt:
                    print("\n\nInput cancelled.")
                    return False
        
        # Save to storage
        if vocab_pairs:
            result = self.storage.add_weekly_vocabulary(week, vocab_pairs, skip_duplicates=False)
            print(f"\n✓ Successfully added {result['added']} vocabulary pairs for Week {week}!")
            if result['skipped'] > 0:
                print(f"⚠ Skipped {result['skipped']} duplicate(s)")
            return True
        return False
    
    def bulk_input_from_text(self, week: int, text_input: str) -> bool:
        """
        Add vocabulary from multi-line text input.
        
        Args:
            week: Week number
            text_input: Multi-line text with format "english norwegian" per line
            
        Returns:
            True if successful, False otherwise
        """
        lines = [line.strip() for line in text_input.strip().split('\n') if line.strip()]
        
        if not lines:
            print("Error: No vocabulary pairs provided")
            return False
        
        vocab_pairs = []
        for i, line in enumerate(lines, 1):
            # Try multiple parsing strategies
            parts = None
            
            # Strategy 1: Split by tab (if present)
            if '\t' in line:
                parts = [p.strip() for p in line.split('\t') if p.strip()]
            
            # Strategy 2: Split by multiple spaces (2 or more)
            elif '  ' in line:
                parts = [p.strip() for p in line.split('  ') if p.strip()][:2]
            
            # Strategy 3: Split on first whitespace
            else:
                parts = line.split(None, 1)
            
            if not parts or len(parts) != 2:
                print(f"Error on line {i}: '{line}' - Expected format: 'english<TAB>norwegian' or 'english  norwegian' (2+ spaces)")
                print(f"   Tip: Avoid single spaces if words contain commas")
                return False
            
            english, norwegian = parts
            
            # Warn about commas (they can break CSV format)
            if ',' in english or ',' in norwegian:
                print(f"⚠️  Line {i}: Contains comma - will be auto-converted to semicolon")
                english = english.replace(',', ';')
                norwegian = norwegian.replace(',', ';')
            
            vocab_pairs.append((english.strip(), norwegian.strip()))
        
        result = self.storage.add_weekly_vocabulary(week, vocab_pairs, skip_duplicates=True)
        
        print(f"\n✓ Successfully added {result['added']} vocabulary pairs for Week {week}!")
        
        if result['skipped'] > 0:
            print(f"⚠ Skipped {result['skipped']} duplicate(s):")
            for dup in result['duplicates']:
                if dup['match_type'] == 'exact':
                    print(f"  - '{dup['english']}' / '{dup['norwegian']}' (exact match in Week {dup['existing_week']})")
                elif dup['match_type'] == 'english_only':
                    print(f"  - '{dup['english']}' (exists in Week {dup['existing_week']} with different translation)")
                elif dup['match_type'] == 'norwegian_only':
                    print(f"  - '{dup['norwegian']}' (exists in Week {dup['existing_week']} with different English)")
        
        return True
    
    def get_available_weeks(self) -> List[int]:
        """Get list of all available weeks."""
        return self.storage.get_all_weeks()
    
    def display_vocabulary(self, week: int):
        """Display vocabulary for a specific week."""
        vocab = self.storage.get_vocabulary_by_week(week)
        
        if not vocab:
            print(f"\nNo vocabulary found for Week {week}.")
            return
        
        print(f"\n=== Vocabulary for Week {week} ===")
        print("-" * 60)
        print(f"{'English':<30} {'Norwegian':<30}")
        print("-" * 60)
        
        for item in vocab:
            print(f"{item['english']:<30} {item['norwegian']:<30}")
        
        print("-" * 60)
        print(f"Total: {len(vocab)} words")
    
    def display_all_weeks(self):
        """Display all available weeks with their vocabulary count."""
        weeks = self.get_available_weeks()
        
        if not weeks:
            print("\nNo vocabulary data available yet.")
            return
        
        print("\n=== Available Weeks ===")
        print("-" * 40)
        
        for week in weeks:
            vocab = self.storage.get_vocabulary_by_week(week)
            print(f"Week {week}: {len(vocab)} words")
        
        print("-" * 40)
