#!/usr/bin/env python3
"""
Launcher script for Vocabulary Trainer GUI
Checks dependencies and starts the app
"""

import sys
import os

def check_dependencies():
    """Check if all required modules are available."""
    required = ['tkinter', 'csv', 'random', 'datetime']
    missing = []
    
    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    return missing

def main():
    """Launch the application."""
    print("="*50)
    print("  🌟 Vocabulary Trainer Starting... 🌟")
    print("="*50)
    print()
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher required!")
        print(f"   You have Python {sys.version_info.major}.{sys.version_info.minor}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Check dependencies
    print("Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"❌ Missing modules: {', '.join(missing)}")
        print("\nPlease install missing dependencies.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("✓ All dependencies found!")
    print()
    
    # Check data directory
    if not os.path.exists('data'):
        print("Creating data directory...")
        os.makedirs('data')
        print("✓ Data directory created!")
    
    print("🚀 Launching GUI...")
    print()
    
    # Import and run
    try:
        from gui import main as run_gui
        run_gui()
    except Exception as e:
        print(f"\n❌ Error starting GUI: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
