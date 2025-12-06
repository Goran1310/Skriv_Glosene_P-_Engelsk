#!/usr/bin/env python3
"""
Skriv Glosene På Engelsk - Norwegian/English Vocabulary Training App
Main application entry point with interactive menu system.
"""

import sys
from storage import VocabularyStorage, ResultsStorage
from vocabulary import VocabularyManager
from quiz import QuizManager


class VocabularyApp:
    """Main application class."""
    
    def __init__(self):
        # Initialize storage
        self.vocab_storage = VocabularyStorage()
        self.results_storage = ResultsStorage()
        
        # Initialize managers
        self.vocab_manager = VocabularyManager(self.vocab_storage)
        self.quiz_manager = QuizManager(self.vocab_storage, self.results_storage)
        
        # Current user
        self.username = None
    
    def set_username(self):
        """Get or confirm username."""
        if not self.username:
            self.username = input("\nEnter your name: ").strip()
            if not self.username:
                self.username = "Student"
            print(f"Welcome, {self.username}!")
    
    def display_main_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("  SKRIV GLOSENE PÅ ENGELSK - Vocabulary Training")
        print("="*60)
        print("1. Add New Weekly Vocabulary")
        print("2. View Vocabulary by Week")
        print("3. View All Available Weeks")
        print("4. Take Quiz - Mode A (Single Week)")
        print("5. Take Quiz - Mode B (Multiple Weeks)")
        print("6. View Quiz Results")
        print("7. View My Results")
        print("8. Change Username")
        print("0. Exit")
        print("="*60)
    
    def add_vocabulary_menu(self):
        """Handle adding new vocabulary."""
        print("\n--- Add New Weekly Vocabulary ---")
        
        # Show existing weeks
        existing_weeks = self.vocab_manager.get_available_weeks()
        if existing_weeks:
            print(f"Existing weeks: {', '.join(map(str, existing_weeks))}")
        
        # Get week number
        while True:
            try:
                week_input = input("\nEnter week number: ").strip()
                week = int(week_input)
                if week < 1:
                    print("Week number must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Check if week already exists
        if week in existing_weeks:
            confirm = input(f"Week {week} already exists. Add more words? (y/n): ").strip().lower()
            if confirm != 'y':
                return
        
        # Get number of words
        while True:
            try:
                num_input = input("\nHow many vocabulary pairs to add? (default: 10): ").strip()
                num_words = int(num_input) if num_input else 10
                if num_words < 1:
                    print("Must add at least 1 word.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Choose input method
        print("\nChoose input method:")
        print("1. Interactive input (one by one)")
        print("2. Bulk paste")
        
        choice = input("Choice (1/2): ").strip()
        
        if choice == '1':
            self.vocab_manager.input_weekly_vocabulary(week, num_words)
        elif choice == '2':
            print(f"\nPaste lines in format: 'english norwegian'")
            print("Example:")
            print("  greedy grådig")
            print("  above all meir enn noko anna")
            print(f"\nPaste up to {num_words} lines and press Enter on empty line when done:")
            print("-" * 50)
            
            lines = []
            empty_count = 0
            while len(lines) < num_words:
                try:
                    line = input()
                    if line.strip():
                        lines.append(line)
                        empty_count = 0
                    else:
                        empty_count += 1
                        if empty_count >= 1 and len(lines) > 0:
                            break
                except EOFError:
                    break
            
            if lines:
                text_input = '\n'.join(lines)
                self.vocab_manager.bulk_input_from_text(week, text_input)
            else:
                print("No vocabulary entered.")
        else:
            print("Invalid choice.")
    
    def view_vocabulary_menu(self):
        """Handle viewing vocabulary by week."""
        existing_weeks = self.vocab_manager.get_available_weeks()
        
        if not existing_weeks:
            print("\nNo vocabulary data available yet.")
            return
        
        print(f"\nAvailable weeks: {', '.join(map(str, existing_weeks))}")
        
        while True:
            try:
                week_input = input("Enter week number to view: ").strip()
                week = int(week_input)
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        self.vocab_manager.display_vocabulary(week)
    
    def quiz_mode_a_menu(self):
        """Handle Mode A quiz."""
        self.set_username()
        
        existing_weeks = self.vocab_manager.get_available_weeks()
        
        if not existing_weeks:
            print("\nNo vocabulary data available yet.")
            return
        
        print(f"\nAvailable weeks: {', '.join(map(str, existing_weeks))}")
        
        while True:
            try:
                week_input = input("Enter week number to practice: ").strip()
                week = int(week_input)
                if week not in existing_weeks:
                    print(f"Week {week} not found.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Ask about randomization
        random_choice = input("Randomize order? (y/n, default=y): ").strip().lower()
        randomize = random_choice != 'n'
        
        self.quiz_manager.run_mode_a(week, self.username, randomize)
    
    def quiz_mode_b_menu(self):
        """Handle Mode B quiz."""
        self.set_username()
        
        existing_weeks = self.vocab_manager.get_available_weeks()
        
        if not existing_weeks:
            print("\nNo vocabulary data available yet.")
            return
        
        print(f"\nAvailable weeks: {', '.join(map(str, existing_weeks))}")
        print(f"Total weeks available: {len(existing_weeks)}")
        
        while True:
            try:
                num_input = input("How many recent weeks to practice? ").strip()
                num_weeks = int(num_input)
                if num_weeks < 1:
                    print("Must be at least 1 week.")
                    continue
                if num_weeks > len(existing_weeks):
                    print(f"Only {len(existing_weeks)} weeks available. Using all.")
                    num_weeks = len(existing_weeks)
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        self.quiz_manager.run_mode_b(num_weeks, self.username)
    
    def view_all_results(self):
        """View all quiz results."""
        results = self.results_storage.get_all_results()
        self.results_storage.display_results(results)
    
    def view_my_results(self):
        """View results for current user."""
        self.set_username()
        results = self.results_storage.get_results_by_user(self.username)
        
        if not results:
            print(f"\nNo results found for {self.username}.")
        else:
            print(f"\nResults for {self.username}:")
            self.results_storage.display_results(results)
    
    def run(self):
        """Main application loop."""
        print("\n" + "="*60)
        print("  Welcome to Skriv Glosene På Engelsk!")
        print("  Norwegian/English Vocabulary Training System")
        print("="*60)
        
        while True:
            self.display_main_menu()
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.add_vocabulary_menu()
            elif choice == '2':
                self.view_vocabulary_menu()
            elif choice == '3':
                self.vocab_manager.display_all_weeks()
            elif choice == '4':
                self.quiz_mode_a_menu()
            elif choice == '5':
                self.quiz_mode_b_menu()
            elif choice == '6':
                self.view_all_results()
            elif choice == '7':
                self.view_my_results()
            elif choice == '8':
                self.username = None
                self.set_username()
            elif choice == '0':
                print("\nThank you for using the vocabulary trainer!")
                print("Lykke til! (Good luck!)")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please try again.")


def main():
    """Application entry point."""
    try:
        app = VocabularyApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
