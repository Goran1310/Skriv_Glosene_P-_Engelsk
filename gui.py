"""
Kid-Friendly GUI for Skriv Glosene På Engelsk
Colorful, easy-to-use interface for 12-year-olds
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import time
from storage import VocabularyStorage, ResultsStorage, ScoreStorageJSON
from vocabulary import VocabularyManager
from quiz import QuizManager


class VocabularyAppGUI:
    """Main GUI application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🇳🇴 Skriv Glosene På Engelsk! 🇬🇧")
        self.root.geometry("800x600")
        
        # Initialize storage and managers
        self.vocab_storage = VocabularyStorage()
        self.results_storage = ResultsStorage()
        self.score_storage = ScoreStorageJSON()  # New JSON score storage
        self.vocab_manager = VocabularyManager(self.vocab_storage)
        self.quiz_manager = QuizManager(self.vocab_storage, self.results_storage)
        
        # User settings
        self.username = tk.StringVar(value="Student")
        
        # Quiz timing
        self.quiz_start_time = None

        # Colors - bright and friendly
        self.colors = {
            'bg': '#E8F4F8',           # Light blue background
            'primary': '#4A90E2',      # Bright blue
            'secondary': '#50C878',    # Emerald green
            'warning': '#FFB347',      # Pastel orange
            'danger': '#FF6B6B',       # Coral red
            'success': '#90EE90',      # Light green
            'header': '#2E5266',       # Dark blue
            'text': '#2C3E50',         # Dark gray
            'white': '#FFFFFF'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Setup fonts
        self.setup_fonts()
        
        # Show main menu
        self.show_main_menu()
    
    def setup_fonts(self):
        """Setup custom fonts."""
        self.fonts = {
            'title': font.Font(family='Comic Sans MS', size=26, weight='bold'),
            'header': font.Font(family='Arial', size=20, weight='bold'),
            'normal': font.Font(family='Arial', size=13),
            'button': font.Font(family='Arial', size=15, weight='bold'),
            'small': font.Font(family='Arial', size=11)
        }
    
    def clear_window(self):
        """Clear all widgets from window."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_header(self, text, emoji="🎓"):
        """Create a colorful header."""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text=f"{emoji} {text} {emoji}",
            font=self.fonts['title'],
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        header_label.pack(expand=True)
    
    def create_button(self, parent, text, command, color=None, emoji=""):
        """Create a styled button."""
        if color is None:
            color = self.colors['primary']
        
        btn = tk.Button(
            parent,
            text=f"{emoji} {text}",
            command=command,
            font=self.fonts['button'],
            bg=color,
            fg=self.colors['white'],
            activebackground=color,
            activeforeground=self.colors['white'],
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=15,
            cursor='hand2'
        )
        return btn
    
    def show_main_menu(self):
        """Display the main menu."""
        self.clear_window()
        self.create_header("Vocabulary Trainer!", "🌟")
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        # Welcome message
        welcome = tk.Label(
            main_frame,
            text=f"Welcome, {self.username.get()}! 👋",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.colors['header']
        )
        welcome.pack(pady=(0, 30))
        
        # Button container
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(expand=True)
        
        # Buttons in a grid
        buttons = [
            ("📝 Add New Words", self.show_add_vocabulary, self.colors['secondary']),
            ("👀 View My Words", self.show_view_vocabulary, self.colors['primary']),
            ("🎮 Take a Quiz!", self.show_quiz_menu, self.colors['warning']),
            ("📊 My Scores", self.show_results, self.colors['danger']),
            ("⚙️ Settings", self.show_settings, self.colors['header']),
            ("👋 Exit", self.root.quit, self.colors['text'])
        ]
        
        for i, (text, cmd, color) in enumerate(buttons):
            btn = self.create_button(button_frame, text.split(maxsplit=1)[1], cmd, color, text.split()[0])
            btn.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='ew')
            button_frame.grid_columnconfigure(i%2, weight=1)
        
        # Stats at bottom
        self.show_stats_footer(main_frame)
    
    def show_stats_footer(self, parent):
        """Show quick stats at bottom."""
        stats_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RIDGE, bd=2)
        stats_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        weeks = self.vocab_manager.get_available_weeks()
        total_words = sum(len(self.vocab_storage.get_vocabulary_by_week(w)) for w in weeks)
        
        stats_text = f"📚 Weeks: {len(weeks)} | 📖 Total Words: {total_words}"
        stats_label = tk.Label(
            stats_frame,
            text=stats_text,
            font=self.fonts['normal'],
            bg=self.colors['white'],
            fg=self.colors['text'],
            pady=10
        )
        stats_label.pack()
    
    def show_add_vocabulary(self):
        """Show add vocabulary screen."""
        self.clear_window()
        self.create_header("Add New Words", "📝")
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        # Week selection
        week_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        week_frame.pack(pady=20)
        
        tk.Label(
            week_frame,
            text="Which week? 📅",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.colors['header']
        ).pack()
        
        week_var = tk.StringVar()
        week_entry = tk.Entry(
            week_frame,
            textvariable=week_var,
            font=self.fonts['normal'],
            width=10,
            justify='center'
        )
        week_entry.pack(pady=10)
        week_entry.focus()
        
        # Existing weeks info
        weeks = self.vocab_manager.get_available_weeks()
        if weeks:
            existing_label = tk.Label(
                week_frame,
                text=f"You have: {', '.join(map(str, weeks))}",
                font=self.fonts['small'],
                bg=self.colors['bg'],
                fg=self.colors['text']
            )
            existing_label.pack()
        
        # Input area
        input_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RIDGE, bd=2)
        input_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            input_frame,
            text="Type your words (one per line):\nFormat: english word → norwegian ord",
            font=self.fonts['normal'],
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        # Text area with scrollbar
        text_frame = tk.Frame(input_frame, bg=self.colors['white'])
        text_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_area = tk.Text(
            text_frame,
            font=self.fonts['normal'],
            height=10,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_area.yview)
        
        # Example text
        example_text = """happy → glad
sad → trist
for instance → for eksempel"""
        text_area.insert('1.0', example_text)
        text_area.tag_add("example", "1.0", "end")
        text_area.tag_config("example", foreground="gray")
        
        def clear_example(event):
            if text_area.get('1.0', 'end-1c') == example_text:
                text_area.delete('1.0', 'end')
                text_area.tag_remove("example", "1.0", "end")
        
        text_area.bind('<FocusIn>', clear_example)
        
        # Button frame
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        def save_words():
            week_str = week_var.get().strip()
            if not week_str:
                messagebox.showerror("Oops!", "Please enter a week number! 📅")
                return
            
            try:
                week = int(week_str)
            except ValueError:
                messagebox.showerror("Oops!", "Week must be a number! 🔢")
                return
            
            text = text_area.get('1.0', 'end-1c').strip()
            if not text or text == example_text:
                messagebox.showerror("Oops!", "Please add some words first! ✍️")
                return
            
            # Parse vocabulary
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            vocab_pairs = []
            
            for i, line in enumerate(lines, 1):
                # Try different separators
                if '→' in line:
                    parts = line.split('→')
                elif '\t' in line:
                    parts = line.split('\t')
                elif '  ' in line:
                    parts = line.split('  ')
                else:
                    parts = line.split(None, 1)
                
                if len(parts) == 2:
                    english = parts[0].strip()
                    norwegian = parts[1].strip()
                    
                    # Auto-convert commas
                    if ',' in english:
                        english = english.replace(',', ';')
                    if ',' in norwegian:
                        norwegian = norwegian.replace(',', ';')
                    
                    vocab_pairs.append((english, norwegian))
                else:
                    messagebox.showwarning(
                        "Hmm...",
                        f"Line {i} looks weird:\n'{line}'\n\nUse: english → norwegian"
                    )
                    return
            
            if not vocab_pairs:
                messagebox.showerror("Oops!", "No valid words found! ✍️")
                return
            
            # Save
            result = self.vocab_storage.add_weekly_vocabulary(week, vocab_pairs, skip_duplicates=True)
            
            msg = f"🎉 Awesome!\n\nAdded {result['added']} new words to Week {week}!"
            if result['skipped'] > 0:
                msg += f"\n\n⚠️ Skipped {result['skipped']} duplicates"
            
            messagebox.showinfo("Success!", msg)
            self.show_main_menu()
        
        def cancel():
            """Cancel and go back without saving."""
            if messagebox.askyesno("Cancel?", "Go back without saving? 🤔"):
                self.show_main_menu()
        
        self.create_button(btn_frame, "Save Words", save_words, self.colors['success'], "💾").pack(side=tk.LEFT, padx=10)
        self.create_button(btn_frame, "Cancel", cancel, self.colors['warning'], "❌").pack(side=tk.LEFT, padx=10)
        self.create_button(btn_frame, "Back", self.show_main_menu, self.colors['text'], "◀").pack(side=tk.LEFT, padx=10)
    
    def show_view_vocabulary(self):
        """Show vocabulary viewer."""
        self.clear_window()
        self.create_header("My Word Lists", "📚")
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        weeks = self.vocab_manager.get_available_weeks()
        
        if not weeks:
            tk.Label(
                main_frame,
                text="No words yet! 📝\nAdd some words first!",
                font=self.fonts['header'],
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(expand=True)
            
            self.create_button(main_frame, "Back", self.show_main_menu, self.colors['text'], "◀").pack(pady=20)
            return
        
        # Week selection
        tk.Label(
            main_frame,
            text="Choose a week:",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.colors['header']
        ).pack(pady=10)
        
        week_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        week_frame.pack(pady=10)
        
        selected_week = tk.IntVar(value=weeks[-1])
        
        for week in weeks:
            count = len(self.vocab_storage.get_vocabulary_by_week(week))
            tk.Radiobutton(
                week_frame,
                text=f"Week {week} ({count} words)",
                variable=selected_week,
                value=week,
                font=self.fonts['normal'],
                bg=self.colors['bg'],
                selectcolor=self.colors['success']
            ).pack(anchor=tk.W, padx=20)
        
        # Display area
        display_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RIDGE, bd=2)
        display_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Create Treeview
        tree_frame = tk.Frame(display_frame, bg=self.colors['white'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=('English', 'Norwegian'),
            show='headings',
            yscrollcommand=tree_scroll.set,
            height=10
        )
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('English', text='🇬🇧 English')
        tree.heading('Norwegian', text='🇳🇴 Norwegian')
        tree.column('English', width=300)
        tree.column('Norwegian', width=300)
        
        def load_vocab():
            tree.delete(*tree.get_children())
            vocab = self.vocab_storage.get_vocabulary_by_week(selected_week.get())
            for item in vocab:
                tree.insert('', 'end', values=(item['english'], item['norwegian']))
        
        load_vocab()
        
        # Refresh button
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        self.create_button(btn_frame, "Refresh", load_vocab, self.colors['primary'], "🔄").pack(side=tk.LEFT, padx=10)
        self.create_button(btn_frame, "Back", self.show_main_menu, self.colors['text'], "◀").pack(side=tk.LEFT, padx=10)
    
    def show_quiz_menu(self):
        """Show quiz mode selection."""
        self.clear_window()
        self.create_header("Time to Practice!", "🎮")
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        weeks = self.vocab_manager.get_available_weeks()
        
        if not weeks:
            tk.Label(
                main_frame,
                text="No words to quiz! 📝\nAdd some words first!",
                font=self.fonts['header'],
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(expand=True)
            
            self.create_button(main_frame, "Back", self.show_main_menu, self.colors['text'], "◀").pack(pady=20)
            return
        
        # Mode selection
        tk.Label(
            main_frame,
            text="Choose your challenge:",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.colors['header']
        ).pack(pady=20)
        
        # Mode A button
        mode_a_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RAISED, bd=3)
        mode_a_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(
            mode_a_frame,
            text="🎯 Mode A: Single Week",
            font=self.fonts['header'],
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(pady=5)
        
        tk.Label(
            mode_a_frame,
            text="Practice words from one week",
            font=self.fonts['small'],
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack()
        
        self.create_button(mode_a_frame, "Start Mode A", lambda: self.start_quiz_mode_a(weeks), self.colors['primary']).pack(pady=10)
        
        # Mode B button
        mode_b_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RAISED, bd=3)
        mode_b_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(
            mode_b_frame,
            text="🔥 Mode B: Multiple Weeks",
            font=self.fonts['header'],
            bg=self.colors['white'],
            fg=self.colors['warning']
        ).pack(pady=5)
        
        tk.Label(
            mode_b_frame,
            text="Challenge yourself with mixed weeks!",
            font=self.fonts['small'],
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack()
        
        self.create_button(mode_b_frame, "Start Mode B", lambda: self.start_quiz_mode_b(weeks), self.colors['warning']).pack(pady=10)
        
        # Back button
        self.create_button(main_frame, "Back", self.show_main_menu, self.colors['text'], "◀").pack(pady=20)
    
    def start_quiz_mode_a(self, weeks):
        """Start Mode A quiz."""
        # Week selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Choose Week")
        dialog.geometry("400x600")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Which week to practice?",
            font=self.fonts['header'],
            bg=self.colors['bg']
        ).pack(pady=20)
        
        selected_week = tk.IntVar(value=weeks[-1])
        
        for week in weeks:
            count = len(self.vocab_storage.get_vocabulary_by_week(week))
            tk.Radiobutton(
                dialog,
                text=f"Week {week} ({count} words)",
                variable=selected_week,
                value=week,
                font=self.fonts['normal'],
                bg=self.colors['bg']
            ).pack(anchor=tk.W, padx=40)
        
        # Direction selection
        tk.Label(
            dialog,
            text="\nQuiz Direction:",
            font=self.fonts['normal'],
            bg=self.colors['bg']
        ).pack(pady=(20, 5))
        
        direction_var = tk.StringVar(value="NO→EN")
        tk.Radiobutton(
            dialog,
            text="🇳🇴 Norwegian → English",
            variable=direction_var,
            value="NO→EN",
            font=self.fonts['normal'],
            bg=self.colors['bg']
        ).pack(anchor=tk.W, padx=40)
        
        tk.Radiobutton(
            dialog,
            text="🇬🇧 English → Norwegian",
            variable=direction_var,
            value="EN→NO",
            font=self.fonts['normal'],
            bg=self.colors['bg']
        ).pack(anchor=tk.W, padx=40)
        
        randomize_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            dialog,
            text="🔀 Randomize order",
            variable=randomize_var,
            font=self.fonts['normal'],
            bg=self.colors['bg']
        ).pack(pady=20)
        
        def start():
            dialog.destroy()
            self.run_quiz(selected_week.get(), randomize_var.get(), direction_var.get())
        
        self.create_button(dialog, "Start Quiz!", start, self.colors['success'], "🚀").pack(pady=10)
        tk.Button(dialog, text="Cancel", command=dialog.destroy).pack()
    
    def start_quiz_mode_b(self, weeks):
        """Start Mode B quiz."""
        # Number of weeks dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Choose Weeks")
        dialog.geometry("400x400")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="How many recent weeks?",
            font=self.fonts['header'],
            bg=self.colors['bg']
        ).pack(pady=20)
        
        num_var = tk.IntVar(value=min(3, len(weeks)))
        
        scale = tk.Scale(
            dialog,
            from_=1,
            to=len(weeks),
            orient=tk.HORIZONTAL,
            variable=num_var,
            length=300,
            font=self.fonts['normal'],
            bg=self.colors['bg']
        )
        scale.pack(pady=20)
        
        # Direction selection
        tk.Label(
            dialog,
            text="Quiz Direction:",
            font=self.fonts['normal'],
            bg=self.colors['bg']
        ).pack(pady=(10, 5))
        
        direction_var = tk.StringVar(value="NO→EN")
        tk.Radiobutton(
            dialog,
            text="🇳🇴 Norwegian → English",
            variable=direction_var,
            value="NO→EN",
            font=self.fonts['normal'],
            bg=self.colors['bg']
        ).pack(anchor=tk.W, padx=40)
        
        tk.Radiobutton(
            dialog,
            text="🇬🇧 English → Norwegian",
            variable=direction_var,
            value="EN→NO",
            font=self.fonts['normal'],
            bg=self.colors['bg']
        ).pack(anchor=tk.W, padx=40)
        
        def start():
            dialog.destroy()
            self.run_quiz_multi(num_var.get(), direction_var.get())
        
        self.create_button(dialog, "Start Quiz!", start, self.colors['success'], "🚀").pack(pady=10)
        tk.Button(dialog, text="Cancel", command=dialog.destroy).pack()
    
    def run_quiz(self, week, randomize, direction="NO→EN"):
        """Run a quiz for single week."""
        vocab = self.vocab_storage.get_vocabulary_by_week(week)
        
        if not vocab:
            messagebox.showerror("Oops!", f"No words found for Week {week}!")
            return
        
        # Create questions based on selected direction
        questions = []
        for item in vocab:
            if direction == "NO→EN":
                questions.append({
                    'question': item['norwegian'],
                    'answer': item['english'],
                    'direction': 'NO→EN'
                })
            else:
                questions.append({
                    'question': item['english'],
                    'answer': item['norwegian'],
                    'direction': 'EN→NO'
                })
        
        if randomize:
            random.shuffle(questions)
        
        self.show_quiz_screen(questions, f"Week {week}", f"Mode A ({'Random' if randomize else 'Sequential'})")
    
    def run_quiz_multi(self, num_weeks, direction="NO→EN"):
        """Run quiz for multiple weeks."""
        all_weeks = self.vocab_storage.get_all_weeks()
        selected_weeks = all_weeks[-num_weeks:]
        
        vocab = self.vocab_storage.get_vocabulary_by_weeks(selected_weeks)
        
        if not vocab:
            messagebox.showerror("Oops!", "No words found!")
            return
        
        # Create questions based on selected direction
        questions = []
        for item in vocab:
            if direction == "NO→EN":
                questions.append({
                    'question': item['norwegian'],
                    'answer': item['english'],
                    'direction': 'NO→EN'
                })
            else:
                questions.append({
                    'question': item['english'],
                    'answer': item['norwegian'],
                    'direction': 'EN→NO'
                })
        
        random.shuffle(questions)
        
        weeks_str = f"Weeks {min(selected_weeks)}-{max(selected_weeks)}"
        self.show_quiz_screen(questions, weeks_str, "Mode B (Multi-week)")
    
    def show_quiz_screen(self, questions, weeks_info, mode_name):
        """Display quiz screen."""
        self.clear_window()
        self.create_header("Quiz Time!", "🎯")
        
        # Start timer
        self.quiz_start_time = time.time()
        quiz_direction = questions[0]['direction'] if questions else "mixed"
        
        current_q = {'index': 0, 'correct': 0}
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        # Progress
        progress_label = tk.Label(
            main_frame,
            text="",
            font=self.fonts['normal'],
            bg=self.colors['bg'],
            fg=self.colors['header']
        )
        progress_label.pack(pady=10)
        
        # Question display
        question_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RAISED, bd=3)
        question_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        direction_label = tk.Label(
            question_frame,
            text="",
            font=self.fonts['small'],
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        direction_label.pack(pady=10)
        
        question_label = tk.Label(
            question_frame,
            text="",
            font=self.fonts['title'],
            bg=self.colors['white'],
            fg=self.colors['primary'],
            wraplength=600
        )
        question_label.pack(pady=30)
        
        # Hint label (underscores for answer length)
        hint_label = tk.Label(
            question_frame,
            text="",
            font=font.Font(family='Courier New', size=14),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        hint_label.pack(pady=10)
        
        # Answer entry
        answer_var = tk.StringVar()
        answer_entry = tk.Entry(
            question_frame,
            textvariable=answer_var,
            font=font.Font(size=16),
            width=30,
            justify='center'
        )
        answer_entry.pack(pady=20)
        
        feedback_label = tk.Label(
            question_frame,
            text="",
            font=self.fonts['header'],
            bg=self.colors['white']
        )
        feedback_label.pack(pady=10)
        
        def check_answer():
            user_answer = answer_var.get().strip()
            correct_answer = questions[current_q['index']]['answer']
            
            # Simple check (case-insensitive)
            if user_answer.lower() == correct_answer.lower():
                feedback_label.config(text="✅ Correct! Great job!", fg=self.colors['success'])
                current_q['correct'] += 1
            else:
                feedback_label.config(
                    text=f"❌ Oops! It was: {correct_answer}",
                    fg=self.colors['danger']
                )
            
            submit_btn.config(state='disabled')
            self.root.after(2000, next_question)
        
        def next_question():
            current_q['index'] += 1
            
            if current_q['index'] >= len(questions):
                show_results()
                return
            
            # Update question
            q = questions[current_q['index']]
            progress_label.config(text=f"Question {current_q['index'] + 1} of {len(questions)} | Score: {current_q['correct']}/{current_q['index']}")
            direction_label.config(text=q['direction'])
            question_label.config(text=q['question'])
            
            # Create hint with underscores for each letter
            answer_length = len(q['answer'])
            hint_text = ''.join(['_ ' if c.isalnum() else f'{c} ' for c in q['answer']])
            hint_label.config(text=hint_text.strip())
            
            answer_var.set('')
            feedback_label.config(text='')
            submit_btn.config(state='normal')
            answer_entry.focus()
        
        def show_results():
            score_pct = (current_q['correct'] / len(questions)) * 100
            
            # Calculate time taken
            time_taken = int(time.time() - self.quiz_start_time) if self.quiz_start_time else None
            
            # Save to CSV (legacy)
            self.results_storage.save_result(
                self.username.get(),
                mode_name,
                weeks_info,
                len(questions),
                current_q['correct']
            )
            
            # Save to JSON with detailed info
            self.score_storage.save_score(
                username=self.username.get(),
                mode=mode_name,
                weeks=weeks_info,
                total_questions=len(questions),
                correct_answers=current_q['correct'],
                time_taken_seconds=time_taken,
                direction=quiz_direction
            )
            
            # Show result screen
            self.clear_window()
            self.create_header("Quiz Complete!", "🎉")
            
            result_frame = tk.Frame(self.root, bg=self.colors['bg'])
            result_frame.pack(expand=True)
            
            # Emoji based on score
            if score_pct == 100:
                emoji = "🏆"
                msg = "PERFECT! You're amazing!"
            elif score_pct >= 80:
                emoji = "⭐"
                msg = "Excellent work!"
            elif score_pct >= 60:
                emoji = "👍"
                msg = "Good job!"
            else:
                emoji = "💪"
                msg = "Keep practicing!"
            
            tk.Label(
                result_frame,
                text=emoji,
                font=font.Font(size=72),
                bg=self.colors['bg']
            ).pack(pady=20)
            
            tk.Label(
                result_frame,
                text=msg,
                font=self.fonts['title'],
                bg=self.colors['bg'],
                fg=self.colors['header']
            ).pack()
            
            tk.Label(
                result_frame,
                text=f"Score: {current_q['correct']}/{len(questions)} ({score_pct:.0f}%)",
                font=self.fonts['header'],
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(pady=20)
            
            btn_frame = tk.Frame(result_frame, bg=self.colors['bg'])
            btn_frame.pack(pady=30)
            
            self.create_button(btn_frame, "Quiz Again", self.show_quiz_menu, self.colors['primary'], "🔄").pack(side=tk.LEFT, padx=10)
            self.create_button(btn_frame, "Main Menu", self.show_main_menu, self.colors['success'], "🏠").pack(side=tk.LEFT, padx=10)
        
        submit_btn = self.create_button(question_frame, "Check Answer", check_answer, self.colors['success'], "✓")
        submit_btn.pack(pady=20)
        
        answer_entry.bind('<Return>', lambda e: check_answer())
        
        # Start first question
        next_question()
    
    def show_results(self):
        """Show results history with JSON-based statistics."""
        self.clear_window()
        self.create_header("My Scores", "📊")
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        # Get user stats from JSON
        user_stats = self.score_storage.get_user_stats(self.username.get())
        scores = self.score_storage.get_user_scores(self.username.get())
        
        if not scores:
            tk.Label(
                main_frame,
                text="No quiz results yet! 🎮\nTake a quiz to see your scores!",
                font=self.fonts['header'],
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(expand=True)
            
            self.create_button(main_frame, "Back", self.show_main_menu, self.colors['text'], "◀").pack(pady=20)
            return
        
        # User statistics panel
        if user_stats:
            stats_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RAISED, bd=3)
            stats_frame.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(
                stats_frame,
                text=f"📈 {self.username.get()}'s Statistics",
                font=self.fonts['header'],
                bg=self.colors['white'],
                fg=self.colors['primary']
            ).pack(pady=10)
            
            stats_grid = tk.Frame(stats_frame, bg=self.colors['white'])
            stats_grid.pack(pady=10, padx=20)
            
            stats_items = [
                ("Total Quizzes:", f"{user_stats['total_quizzes']}"),
                ("Average Score:", f"{user_stats['average_score']}%"),
                ("Best Score:", f"{user_stats['best_score']}%"),
                ("Total Questions:", f"{user_stats['total_questions']}")
            ]
            
            for i, (label, value) in enumerate(stats_items):
                tk.Label(
                    stats_grid,
                    text=label,
                    font=self.fonts['normal'],
                    bg=self.colors['white'],
                    fg=self.colors['text']
                ).grid(row=i//2, column=(i%2)*2, padx=10, pady=5, sticky=tk.W)
                
                tk.Label(
                    stats_grid,
                    text=value,
                    font=font.Font(size=12, weight='bold'),
                    bg=self.colors['white'],
                    fg=self.colors['primary']
                ).grid(row=i//2, column=(i%2)*2+1, padx=10, pady=5, sticky=tk.W)
        
        # Recent scores table
        tk.Label(
            main_frame,
            text="📜 Recent Quizzes (Last 10)",
            font=self.fonts['header'],
            bg=self.colors['bg'],
            fg=self.colors['header']
        ).pack(pady=(10, 5))
        
        tree_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RIDGE, bd=2)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=('Date', 'Weeks', 'Direction', 'Score', 'Time'),
            show='headings',
            yscrollcommand=tree_scroll.set
        )
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('Date', text='📅 Date')
        tree.heading('Weeks', text='📚 Weeks')
        tree.heading('Direction', text='🔄 Direction')
        tree.heading('Score', text='✓ Score')
        tree.heading('Time', text='⏱️ Time')
        
        tree.column('Date', width=100)
        tree.column('Weeks', width=120)
        tree.column('Direction', width=80)
        tree.column('Score', width=100)
        tree.column('Time', width=80)
        
        for score in reversed(scores[-10:]):  # Last 10 results
            time_str = f"{score.get('time_taken_seconds', 0)}s" if score.get('time_taken_seconds') else "-"
            tree.insert('', 'end', values=(
                score['date'],
                score['weeks'],
                score.get('direction', 'mixed'),
                f"{score['correct_answers']}/{score['total_questions']} ({score['score_percentage']}%)",
                time_str
            ))
        
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        self.create_button(btn_frame, "Export Data", lambda: self.export_user_data(), self.colors['secondary'], "💾").pack(side=tk.LEFT, padx=5)
        self.create_button(btn_frame, "Back", self.show_main_menu, self.colors['text'], "◀").pack(side=tk.LEFT, padx=5)
    
    def export_user_data(self):
        """Export user data to JSON file."""
        try:
            export_path = self.score_storage.export_user_data(self.username.get())
            messagebox.showinfo(
                "Success! 💾",
                f"Data exported successfully!\n\nSaved to:\n{export_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data:\n{str(e)}")
    
    def show_settings(self):
        """Show settings screen."""
        self.clear_window()
        self.create_header("Settings", "⚙️")
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        # Username setting
        username_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RIDGE, bd=2)
        username_frame.pack(pady=20, fill=tk.X)
        
        tk.Label(
            username_frame,
            text="Your Name:",
            font=self.fonts['header'],
            bg=self.colors['white']
        ).pack(pady=10)
        
        name_entry = tk.Entry(
            username_frame,
            textvariable=self.username,
            font=self.fonts['normal'],
            width=20,
            justify='center'
        )
        name_entry.pack(pady=10)
        
        def save_settings():
            messagebox.showinfo("Saved!", "Settings saved! ✓")
            self.show_main_menu()
        
        self.create_button(username_frame, "Save", save_settings, self.colors['success'], "💾").pack(pady=10)
        
        self.create_button(main_frame, "Back", self.show_main_menu, self.colors['text'], "◀").pack(pady=20)


def main():
    """Run the GUI application."""
    root = tk.Tk()
    app = VocabularyAppGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
