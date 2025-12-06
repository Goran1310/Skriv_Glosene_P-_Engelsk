"""
Example script showing how to programmatically add vocabulary to the system.
"""

from storage import VocabularyStorage
from vocabulary import VocabularyManager

# Example vocabulary for Week 1 (from your original data)
week_1_vocab = [
    ("greedy", "grådig"),
    ("above all", "meir enn noko anna"),
    ("selfish", "egoistisk"),
    ("spirits", "ånder"),
    ("regretful", "angrande"),
    ("ashamed", "skamfull"),
    ("positively", "til og med, sanneleg"),
    ("grateful", "takknemleg"),
    ("various", "forskjellige"),
    ("rush of happiness", "lykkerus")
]

# Example vocabulary for Week 2
week_2_vocab = [
    ("happy", "glad"),
    ("sad", "trist"),
    ("angry", "sint"),
    ("tired", "trøtt"),
    ("hungry", "sulten"),
    ("thirsty", "tørst"),
    ("cold", "kald"),
    ("warm", "varm"),
    ("beautiful", "vakker"),
    ("ugly", "stygg")
]

def populate_example_data():
    """Add example vocabulary to the database."""
    storage = VocabularyStorage()
    manager = VocabularyManager(storage)
    
    # Add Week 1
    print("Adding Week 1 vocabulary...")
    storage.add_weekly_vocabulary(1, week_1_vocab)
    print("✓ Week 1 added")
    
    # Add Week 2
    print("Adding Week 2 vocabulary...")
    storage.add_weekly_vocabulary(2, week_2_vocab)
    print("✓ Week 2 added")
    
    # Display results
    print("\nVocabulary successfully added!")
    manager.display_all_weeks()
    
    print("\n--- Week 1 Details ---")
    manager.display_vocabulary(1)
    
    print("\n--- Week 2 Details ---")
    manager.display_vocabulary(2)

if __name__ == "__main__":
    populate_example_data()
