"""
Automated data cleaning tool for vocabulary.csv
Fixes CSV structure, multi-word entries, capitalization, and column direction issues.
"""

import csv
import shutil
from datetime import datetime
from pathlib import Path


class VocabularyDataCleaner:
    """Clean and validate vocabulary data."""
    
    def __init__(self, input_file='data/vocabulary.csv'):
        self.input_file = input_file
        self.backup_file = None
        self.issues_found = []
        self.fixes_applied = []
    
    def create_backup(self):
        """Create timestamped backup of original file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_file = f'data/vocabulary_backup_{timestamp}.csv'
        shutil.copy2(self.input_file, self.backup_file)
        print(f"✓ Backup created: {self.backup_file}")
    
    def read_raw_file(self):
        """Read file handling CSV parsing issues."""
        entries = []
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Skip header
        for i, line in enumerate(lines[1:], start=2):
            line = line.strip()
            if not line:
                continue
            
            # Try to parse with csv module first
            try:
                reader = csv.reader([line])
                parts = next(reader)
                
                if len(parts) >= 3:
                    week = parts[0]
                    english = parts[1]
                    norwegian = ' '.join(parts[2:])  # Join any extra parts
                    entries.append({
                        'line': i,
                        'week': week,
                        'english': english.strip(),
                        'norwegian': norwegian.strip(),
                        'original': line
                    })
                elif len(parts) == 2:
                    # Missing column - try to split differently
                    self.issues_found.append(f"Line {i}: Only 2 columns found")
                    entries.append({
                        'line': i,
                        'week': parts[0],
                        'english': parts[1],
                        'norwegian': '',
                        'original': line
                    })
            except Exception as e:
                self.issues_found.append(f"Line {i}: Parse error - {e}")
        
        return entries
    
    def fix_entry(self, entry):
        """Apply fixes to a single entry."""
        week = entry['week']
        english = entry['english'].strip()
        norwegian = entry['norwegian'].strip()
        fixed = False
        
        # Fix Week 39 reversed columns (Norwegian words starting with capital in 'english' column)
        norwegian_indicators = ['kvinne', 'utmerkt', 'usemje', 'ulik', 'imponerande', 
                               'eg', 'spiss', 'gå', 'trene', 'helse']
        if week == '39' and any(english.lower().startswith(word) for word in norwegian_indicators):
            english, norwegian = norwegian, english
            self.fixes_applied.append(f"Line {entry['line']}: Swapped reversed columns")
            fixed = True
        
        # Remove trailing/leading commas
        english = english.strip(',').strip()
        norwegian = norwegian.strip(',').strip()
        
        # Standardize capitalization (lowercase unless proper noun)
        # Keep first letter caps for now, but normalize
        if english and not any(english.startswith(x) for x in ['I ', 'I\'', 'Is ']):
            if english[0].isupper() and ' ' not in english and len(english) > 1:
                # Single word with capital - make lowercase
                original_english = english
                english = english.lower()
                if original_english != english:
                    self.fixes_applied.append(f"Line {entry['line']}: Lowercase English '{original_english}' → '{english}'")
                    fixed = True
        
        # Similar for Norwegian
        if norwegian and norwegian[0].isupper() and ' ' not in norwegian and len(norwegian) > 1:
            original_norwegian = norwegian
            norwegian = norwegian.lower()
            if original_norwegian != norwegian:
                self.fixes_applied.append(f"Line {entry['line']}: Lowercase Norwegian '{original_norwegian}' → '{norwegian}'")
                fixed = True
        
        # Replace commas in translations with semicolons or slashes
        if ',' in norwegian and not norwegian.startswith('"'):
            original = norwegian
            norwegian = norwegian.replace(',', ';')
            self.fixes_applied.append(f"Line {entry['line']}: Replaced commas in Norwegian: '{original}' → '{norwegian}'")
            fixed = True
        
        if ',' in english and not english.startswith('"'):
            original = english
            english = english.replace(',', ';')
            self.fixes_applied.append(f"Line {entry['line']}: Replaced commas in English: '{original}' → '{english}'")
            fixed = True
        
        return {
            'week': week,
            'english': english,
            'norwegian': norwegian,
            'fixed': fixed
        }
    
    def write_cleaned_file(self, entries):
        """Write cleaned data to file."""
        with open(self.input_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['week', 'english', 'norwegian'])
            
            for entry in entries:
                writer.writerow([entry['week'], entry['english'], entry['norwegian']])
        
        print(f"✓ Cleaned data written to: {self.input_file}")
    
    def validate_cleaned_data(self):
        """Validate the cleaned file."""
        issues = []
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=2):
                if not row['english'] or not row['norwegian']:
                    issues.append(f"Line {i}: Missing English or Norwegian")
                
                if ',' in row['english'] or ',' in row['norwegian']:
                    issues.append(f"Line {i}: Still contains commas")
        
        return issues
    
    def clean(self):
        """Main cleaning process."""
        print("\n" + "="*70)
        print("VOCABULARY DATA CLEANING TOOL")
        print("="*70)
        
        # 1. Backup
        print("\n1. Creating backup...")
        self.create_backup()
        
        # 2. Read raw data
        print("\n2. Reading data...")
        entries = self.read_raw_file()
        print(f"   Found {len(entries)} entries")
        
        # 3. Fix entries
        print("\n3. Applying fixes...")
        cleaned_entries = []
        fixes_count = 0
        
        for entry in entries:
            fixed_entry = self.fix_entry(entry)
            cleaned_entries.append(fixed_entry)
            if fixed_entry['fixed']:
                fixes_count += 1
        
        print(f"   Fixed {fixes_count} entries")
        
        # 4. Write cleaned data
        print("\n4. Writing cleaned data...")
        self.write_cleaned_file(cleaned_entries)
        
        # 5. Validate
        print("\n5. Validating...")
        validation_issues = self.validate_cleaned_data()
        
        # 6. Report
        print("\n" + "="*70)
        print("CLEANING REPORT")
        print("="*70)
        
        print(f"\n📊 Statistics:")
        print(f"   Total entries: {len(entries)}")
        print(f"   Entries fixed: {fixes_count}")
        print(f"   Issues found during read: {len(self.issues_found)}")
        print(f"   Fixes applied: {len(self.fixes_applied)}")
        print(f"   Validation issues: {len(validation_issues)}")
        
        if self.issues_found:
            print(f"\n⚠️  Issues found during read:")
            for issue in self.issues_found[:10]:  # Show first 10
                print(f"   - {issue}")
            if len(self.issues_found) > 10:
                print(f"   ... and {len(self.issues_found) - 10} more")
        
        if self.fixes_applied:
            print(f"\n✓ Fixes applied:")
            for fix in self.fixes_applied[:20]:  # Show first 20
                print(f"   - {fix}")
            if len(self.fixes_applied) > 20:
                print(f"   ... and {len(self.fixes_applied) - 20} more")
        
        if validation_issues:
            print(f"\n❌ Validation issues remaining:")
            for issue in validation_issues:
                print(f"   - {issue}")
        else:
            print(f"\n✅ Validation passed - no issues found!")
        
        print(f"\n💾 Backup file: {self.backup_file}")
        print("="*70)
        
        return len(validation_issues) == 0


def main():
    """Run the cleaning tool."""
    cleaner = VocabularyDataCleaner()
    
    try:
        success = cleaner.clean()
        
        if success:
            print("\n✅ Data cleaning completed successfully!")
            print("\nNext steps:")
            print("1. Review the cleaned data in vocabulary.csv")
            print("2. Check DATA_QUALITY_REPORT.md for details")
            print("3. Run: python main.py")
        else:
            print("\n⚠️  Data cleaning completed with warnings.")
            print("   Please review validation issues above.")
            print(f"   Original data backed up to: {cleaner.backup_file}")
        
    except Exception as e:
        print(f"\n❌ Error during cleaning: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
