"""
Qualitative Explanation Inspection

Displays sample explanations for manual validation of automated coding.
Helps verify that feature citations are appropriate, not just keyword matches.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
import random

def inspect_explanations(input_file: Path, n_per_category: int = 3):
    """Display sample explanations for qualitative analysis."""
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    print("="*70)
    print(" QUALITATIVE EXPLANATION INSPECTION")
    print("="*70)
    print("\nShowing sample explanations for manual validation.\n")
    
    categories = ['linguistic', 'physical', 'social', 'dark']
    
    for category in categories:
        cat_explanations = [e for e in data if e['joke_category'] == category and e['success']]
        
        if len(cat_explanations) == 0:
            continue
        
        # Sample randomly
        samples = random.sample(cat_explanations, min(n_per_category, len(cat_explanations)))
        
        print("="*70)
        print(f" {category.upper()} JOKES")
        print("="*70)
        
        for i, expl in enumerate(samples, 1):
            # Get the original joke from pilot data
            print(f"\n{'-'*70}")
            print(f"SAMPLE {i}")
            print(f"{'-'*70}")
            print(f"Joke ID: {expl['joke_id']}")
            print(f"Explaining Model: {expl['explaining_model']}")
            print(f"\nEXPLANATION:")
            print(expl['explanation'])
            
            print(f"\n{'ASSESSMENT QUESTIONS':^70}")
            print("1. Does this explanation cite appropriate features for this category?")
            print("2. Are semantic/embodied/social/threat keywords used correctly?")
            print("3. Does the explanation show actual understanding or just generic analysis?")
            print()
        
        input(f"Press ENTER to see next category...")
    
    print("\n" + "="*70)
    print(" INSPECTION COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("  1. Note which explanations are appropriate vs inappropriate")
    print("  2. Refine keyword lists based on qualitative assessment")
    print("  3. Consider manual coding of subset for validation")
    print("="*70 + "\n")

if __name__ == '__main__':
    output_dir = Path(__file__).parent.parent / 'outputs'
    explanation_files = sorted(output_dir.glob('explanations_*.json'))
    
    if not explanation_files:
        print("Error: No explanation data found!")
        sys.exit(1)
    
    input_file = explanation_files[-1]
    print(f"Using: {input_file.name}\n")
    
    # Show 3 examples per category by default
    n_per_cat = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    
    inspect_explanations(input_file, n_per_category=n_per_cat)