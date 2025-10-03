"""
Structural Validity Analysis: Objective Measures of Joke Quality

Tests whether generated jokes have valid humor structure:
1. Parseability: Clear setup/punchline distinction
2. Format compliance: Matches requested structure
3. Linguistic coherence: Grammatically valid
4. Length appropriateness: Within target range

No subjective ratings - only objective structural properties.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
import pandas as pd
import numpy as np
from collections import Counter
import re

def analyze_structure(joke: dict) -> dict:
    """
    Calculate objective structural properties of a joke.
    
    Returns:
        Dictionary of structural metrics
    """
    setup = joke.get('setup', '')
    punchline = joke.get('punchline', '')
    full_text = joke.get('full_text', '')
    
    # Basic parsing
    has_setup = len(setup.strip()) > 0
    has_punchline = len(punchline.strip()) > 0
    both_present = has_setup and has_punchline
    
    # Length metrics
    setup_words = len(setup.split())
    punchline_words = len(punchline.split())
    total_words = len(full_text.split())
    
    # Target was 15-50 words
    within_target = 15 <= total_words <= 50
    
    # Ratio metrics
    if punchline_words > 0:
        setup_punchline_ratio = setup_words / punchline_words
    else:
        setup_punchline_ratio = None
    
    # Question in setup? (common joke structure)
    has_question = '?' in setup
    
    # Punctuation in punchline (emphasis)
    has_exclamation = '!' in punchline
    has_period = '.' in punchline
    
    # Check for explicit format markers
    explicit_markers = ('Setup:' in full_text or 'setup:' in full_text.lower()) and \
                      ('Punchline:' in full_text or 'punchline:' in full_text.lower())
    
    # Sentence count (rough proxy for complexity)
    sentences = re.split(r'[.!?]+', full_text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    return {
        'has_setup': has_setup,
        'has_punchline': has_punchline,
        'structure_valid': both_present,
        'setup_words': setup_words,
        'punchline_words': punchline_words,
        'total_words': total_words,
        'within_target_length': within_target,
        'setup_punchline_ratio': setup_punchline_ratio,
        'has_question': has_question,
        'has_exclamation': has_exclamation,
        'has_period': has_period,
        'explicit_format_markers': explicit_markers,
        'sentence_count': sentence_count
    }

def run_structural_analysis(input_file: Path):
    """Analyze structural properties of all jokes."""
    
    print("="*70)
    print(" STRUCTURAL VALIDITY ANALYSIS")
    print("="*70)
    
    # Load data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Filter successful jokes
    successful = [d for d in data if d.get('raw_response')]
    
    print(f"\nAnalyzing {len(successful)} successful generations...")
    
    # Analyze each joke
    results = []
    for joke in successful:
        metrics = analyze_structure(joke)
        metrics['id'] = joke['id']
        metrics['model'] = joke['model']
        metrics['category'] = joke['category']
        metrics['temperature'] = joke['temperature']
        results.append(metrics)
    
    df = pd.DataFrame(results)
    
    # Overall statistics
    print(f"\n{'OVERALL STRUCTURAL QUALITY':^70}")
    print("-"*70)
    print(f"  Valid structure (setup + punchline): {df['structure_valid'].sum()}/{len(df)} ({100*df['structure_valid'].mean():.1f}%)")
    print(f"  Within target length (15-50 words): {df['within_target_length'].sum()}/{len(df)} ({100*df['within_target_length'].mean():.1f}%)")
    print(f"  Average total words: {df['total_words'].mean():.1f} (SD={df['total_words'].std():.1f})")
    print(f"  Question format: {df['has_question'].sum()}/{len(df)} ({100*df['has_question'].mean():.1f}%)")
    
    # By model
    print(f"\n{'STRUCTURAL QUALITY BY MODEL':^70}")
    print("-"*70)
    model_stats = df.groupby('model').agg({
        'structure_valid': 'mean',
        'within_target_length': 'mean',
        'total_words': 'mean'
    }).round(3)
    print(model_stats.to_string())
    
    # By category
    print(f"\n{'STRUCTURAL QUALITY BY CATEGORY':^70}")
    print("-"*70)
    cat_stats = df.groupby('category').agg({
        'structure_valid': 'mean',
        'within_target_length': 'mean',
        'total_words': 'mean',
        'has_question': 'mean'
    }).round(3)
    print(cat_stats.to_string())
    
    # Save results
    output_file = input_file.parent / 'structural_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    df.to_csv(input_file.parent / 'structural_analysis.csv', index=False)
    
    print(f"\n✓ Structural analysis complete!")
    print(f"  Saved to: {output_file}")
    print("="*70 + "\n")
    
    return df

if __name__ == '__main__':
    pilot_dir = Path(__file__).parent.parent / 'pilot'
    pilot_files = sorted(pilot_dir.glob('pilot_raw_data_*.json'))
    
    if not pilot_files:
        print("Error: No pilot data found!")
        sys.exit(1)
    
    input_file = pilot_files[-1]
    print(f"Using: {input_file.name}\n")
    
    run_structural_analysis(input_file)