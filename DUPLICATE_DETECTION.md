# Duplicate Detection Feature

## Overview

The vocabulary app now includes comprehensive duplicate detection to prevent adding the same words multiple times and to warn about potential conflicts.

## Features

### 1. **Automatic Duplicate Detection**

When adding vocabulary, the system checks for three types of duplicates:

#### Exact Match
- **What**: Same English word AND same Norwegian translation
- **Example**: "happy" / "glad" already exists
- **Action**: 
  - Interactive mode: Prompts user to confirm if they want to add anyway
  - Bulk mode: Automatically skips and reports

#### English Word Conflict
- **What**: Same English word but different Norwegian translation
- **Example**: "happy" exists as "glad", trying to add "happy" / "lykkelig"
- **Action**: Warns user and prompts for confirmation
- **Use case**: Words with multiple valid translations

#### Norwegian Word Conflict
- **What**: Same Norwegian word but different English translation
- **Example**: "glad" exists as "happy", trying to add "joyful" / "glad"
- **Action**: Warns user and prompts for confirmation
- **Use case**: Norwegian words with multiple English meanings

### 2. **Interactive Mode Behavior**

When adding words one-by-one:
```
1. Enter pair (EN, NO): happy, glad
   ⚠ Duplicate: This exact pair exists in Week 1
   Add anyway? (y/n): n
```

User can choose to:
- Press `n` to skip and enter a different word
- Press `y` to add it anyway (useful for practice repetition)

### 3. **Bulk Mode Behavior**

When pasting multiple words:
- Automatically skips all duplicates
- Shows summary at the end:
  ```
  ✓ Successfully added 8 vocabulary pairs for Week 2!
  ⚠ Skipped 2 duplicate(s):
    - 'happy' / 'glad' (exact match in Week 1)
    - 'sad' (exists in Week 1 with different translation)
  ```

## API Reference

### `VocabularyStorage.check_duplicate()`

```python
def check_duplicate(self, english: str, norwegian: str, week: int = None) -> Dict:
    """
    Check if a vocabulary pair already exists.
    
    Args:
        english: English word/phrase
        norwegian: Norwegian word/phrase
        week: Optional week number to check within specific week only
        
    Returns:
        Dict with:
            'exists' (bool): Whether any duplicate was found
            'week' (int or None): Week number where duplicate exists
            'match_type' (str): 'exact', 'english_only', 'norwegian_only', or None
    """
```

**Example usage:**
```python
storage = VocabularyStorage()
result = storage.check_duplicate("happy", "glad")
print(result)
# {'exists': True, 'week': 1, 'match_type': 'exact'}
```

### `VocabularyStorage.add_weekly_vocabulary()`

```python
def add_weekly_vocabulary(self, week: int, vocab_pairs: List[Tuple[str, str]], 
                         skip_duplicates: bool = True) -> Dict:
    """
    Add vocabulary with duplicate handling.
    
    Args:
        week: Week number
        vocab_pairs: List of (english, norwegian) tuples
        skip_duplicates: If True, automatically skip duplicates
        
    Returns:
        Dict with:
            'added' (int): Number of pairs successfully added
            'skipped' (int): Number of duplicates skipped
            'duplicates' (list): Details about each duplicate found
    """
```

**Example usage:**
```python
vocab = [("happy", "glad"), ("sad", "trist")]
result = storage.add_weekly_vocabulary(1, vocab, skip_duplicates=True)
print(f"Added: {result['added']}, Skipped: {result['skipped']}")
```

## Testing

Run the test script to see duplicate detection in action:

```powershell
python test_duplicates.py
```

This demonstrates:
- Adding initial vocabulary
- Detecting exact duplicates
- Detecting English-only matches
- Detecting Norwegian-only matches
- Automatic skipping in bulk mode

## Use Cases

### 1. **Preventing Accidental Duplicates**
Students won't accidentally add the same word twice, keeping their vocabulary lists clean.

### 2. **Managing Synonyms**
When a word has multiple translations:
- System warns you
- You can decide whether to add both
- Useful for understanding nuances

### 3. **Quality Control**
Bulk imports from text files automatically filter duplicates, showing what was skipped.

### 4. **Cross-Week Learning**
See if you're adding a word you already learned in a previous week.

## Configuration

### Skip Duplicates (Default: True in Bulk Mode)
```python
# Bulk mode: automatically skips
result = storage.add_weekly_vocabulary(week, vocab, skip_duplicates=True)

# Interactive mode: doesn't skip, but prompts user
manager.input_weekly_vocabulary(week, num_words)
```

### Case Insensitive Matching
All duplicate detection is case-insensitive:
- "Happy" = "happy" = "HAPPY"
- "Glad" = "glad" = "GLAD"

## Future Enhancements

Potential improvements:
- [ ] Fuzzy matching for similar words (e.g., "hapiness" vs "happiness")
- [ ] Option to merge duplicates from different weeks
- [ ] Duplicate report showing all duplicates across weeks
- [ ] Allow marking some duplicates as intentional (synonyms)
- [ ] Export duplicate report to CSV

---

**Note**: Duplicate checking makes the vocabulary system more robust and user-friendly, helping students maintain clean, organized vocabulary lists!
