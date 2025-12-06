"""
Manual corrections for vocabulary data.
Fixes multi-word phrases and remaining issues.
"""

import csv
import shutil
from datetime import datetime


# Define manual corrections for problematic entries
CORRECTIONS = {
    # Week 46 corrections
    ('46', 'stuff', 'like that sånne ting'): ('46', 'stuff like that', 'sånne ting'),
    ('46', 'for', 'instance for eksempel'): ('46', 'for instance', 'for eksempel'),
    ('46', 'started', 'yelling begynte å skrike'): ('46', 'started yelling', 'begynte å skrike'),
    
    # Week 45 corrections
    ('45', 'takes', 'care of tar vare på'): ('45', 'takes care of', 'tar vare på'),
    ('45', 'childcare', 'agency barnevernet'): ('45', 'childcare agency', 'barnevernet'),
    ('45', 'straight', 'away med ein gong'): ('45', 'straight away', 'med ein gong'),
    
    # Week 39 corrections (already swapped, just need to fix splits)
    ('39', 'ikkje likeverdig Unequal', 'ulik'): ('39', 'unequal', 'ulik; ikkje likeverdig'),
    ('39', 'meiner In my opinion', 'eg'): ('39', 'in my opinion', 'eg meiner'),
    ('39', 'av med pensjon Retire', 'gå'): ('39', 'retire', 'gå av med pensjon'),
    
    # Week 40 corrections
    ('40', 'is', 'required Trengst; behøvast'): ('40', 'is required', 'trengst; behøvast'),
    ('40', 'Any more Meir', 'lenger'): ('40', 'any more', 'meir; lenger'),
    ('40', 'However', 'Likevel'): ('40', 'however', 'likevel'),
    ('40', 'Lift up', 'Løft opp'): ('40', 'lift up', 'løft opp'),
    ('40', 'Catch', 'Ta i mot'): ('40', 'catch', 'ta i mot'),
}


def apply_manual_corrections():
    """Apply manual corrections to vocabulary data."""
    
    input_file = 'data/vocabulary.csv'
    
    # Create backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'data/vocabulary_manual_backup_{timestamp}.csv'
    shutil.copy2(input_file, backup_file)
    print(f"✓ Backup created: {backup_file}")
    
    # Read current data
    entries = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    
    print(f"✓ Read {len(entries)} entries")
    
    # Apply corrections
    corrections_applied = 0
    corrected_entries = []
    
    for entry in entries:
        week = entry['week']
        english = entry['english']
        norwegian = entry['norwegian']
        
        # Check if this entry needs correction
        key = (week, english, norwegian)
        
        if key in CORRECTIONS:
            new_week, new_english, new_norwegian = CORRECTIONS[key]
            corrected_entries.append({
                'week': new_week,
                'english': new_english,
                'norwegian': new_norwegian
            })
            corrections_applied += 1
            print(f"✓ Corrected Week {week}: '{english}' / '{norwegian}'")
            print(f"  → '{new_english}' / '{new_norwegian}'")
        else:
            corrected_entries.append(entry)
    
    # Write corrected data
    with open(input_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['week', 'english', 'norwegian'])
        writer.writeheader()
        writer.writerows(corrected_entries)
    
    print(f"\n✓ Applied {corrections_applied} manual corrections")
    print(f"✓ Updated file: {input_file}")
    print(f"✓ Backup saved: {backup_file}")
    
    return corrections_applied


def main():
    """Run manual corrections."""
    print("\n" + "="*70)
    print("MANUAL CORRECTIONS TOOL")
    print("="*70)
    print()
    
    try:
        count = apply_manual_corrections()
        
        print("\n" + "="*70)
        if count > 0:
            print("✅ Manual corrections completed successfully!")
            print(f"   {count} entries were corrected")
        else:
            print("ℹ️  No corrections needed - all entries look good!")
        print("="*70)
        
        print("\nNext steps:")
        print("1. Review the corrected data: Get-Content data\\vocabulary.csv")
        print("2. Test the app: python main.py")
        print("3. Check the quality report: cat MANUAL_CORRECTIONS_NEEDED.md")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
