"""
Quick summary of pilot generation results.
Analyzes the raw generated data before manual rating.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
from collections import Counter

def summarize_pilot(filepath: str):
    """Generate summary statistics from pilot data."""
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    print("="*70)
    print(f"{'PILOT GENERATION SUMMARY':^70}")
    print("="*70)
    
    # Overall stats
    total = len(data)
    successful = sum(1 for d in data if d.get('raw_response'))
    failed = total - successful
    
    print(f"\n{'GENERATION STATISTICS':^70}")
    print("-"*70)
    print(f"  Total attempts: {total}")
    print(f"  Successful: {successful} ({100*successful/total:.1f}%)")
    print(f"  Failed: {failed} ({100*failed/total:.1f}%)")
    
    # By model
    print(f"\n{'SUCCESS RATE BY MODEL':^70}")
    print("-"*70)
    model_stats = {}
    for d in data:
        model = d.get('model')
        if model:
            if model not in model_stats:
                model_stats[model] = {'total': 0, 'success': 0}
            model_stats[model]['total'] += 1
            if d.get('raw_response'):
                model_stats[model]['success'] += 1
    
    for model, stats in sorted(model_stats.items()):
        rate = 100 * stats['success'] / stats['total']
        print(f"  {model}: {stats['success']}/{stats['total']} ({rate:.1f}%)")
    
    # By category
    print(f"\n{'SUCCESS RATE BY CATEGORY':^70}")
    print("-"*70)
    cat_stats = {}
    for d in data:
        cat = d.get('category')
        if cat:
            if cat not in cat_stats:
                cat_stats[cat] = {'total': 0, 'success': 0}
            cat_stats[cat]['total'] += 1
            if d.get('raw_response'):
                cat_stats[cat]['success'] += 1
    
    for cat, stats in sorted(cat_stats.items()):
        rate = 100 * stats['success'] / stats['total']
        print(f"  {cat}: {stats['success']}/{stats['total']} ({rate:.1f}%)")
    
    # By temperature
    print(f"\n{'SUCCESS RATE BY TEMPERATURE':^70}")
    print("-"*70)
    temp_stats = {}
    for d in data:
        temp = d.get('temperature')
        if temp:
            if temp not in temp_stats:
                temp_stats[temp] = {'total': 0, 'success': 0}
            temp_stats[temp]['total'] += 1
            if d.get('raw_response'):
                temp_stats[temp]['success'] += 1
    
    for temp, stats in sorted(temp_stats.items()):
        rate = 100 * stats['success'] / stats['total']
        print(f"  {temp}: {stats['success']}/{stats['total']} ({rate:.1f}%)")
    
    # Structural quality
    successful_jokes = [d for d in data if d.get('raw_response')]
    if successful_jokes:
        word_counts = [
            d['metrics'].get('total_words', 0) 
            for d in successful_jokes 
            if d.get('metrics')
        ]
        
        if word_counts:
            print(f"\n{'STRUCTURAL METRICS':^70}")
            print("-"*70)
            print(f"  Average joke length: {sum(word_counts)/len(word_counts):.1f} words")
            print(f"  Shortest: {min(word_counts)} words")
            print(f"  Longest: {max(word_counts)} words")
    
    # Token usage (where available)
    token_counts = [
        d['api_info'].get('tokens', 0)
        for d in data
        if d.get('api_info') and d['api_info'].get('tokens') is not None
    ]
    
    if token_counts:
        print(f"\n{'API USAGE':^70}")
        print("-"*70)
        print(f"  Total tokens (where tracked): {sum(token_counts):,}")
        print(f"  Average per successful call: {sum(token_counts)/len(token_counts):.0f}")
    
    # Show a few examples
    print(f"\n{'SAMPLE GENERATED JOKES':^70}")
    print("-"*70)
    
    # Show one from each category
    categories = ['linguistic', 'physical', 'social', 'dark']
    for cat in categories:
        cat_jokes = [d for d in successful_jokes if d.get('category') == cat]
        if cat_jokes:
            example = cat_jokes[0]
            print(f"\n  {cat.upper()}:")
            print(f"  {example.get('full_text', 'N/A')[:200]}")
    
    print("\n" + "="*70)
    print(f"✓ Data ready for manual rating!")
    print(f"  File: {filepath}")
    print("="*70 + "\n")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        # Find most recent pilot file
        pilot_dir = Path(__file__).parent.parent / 'pilot'
        pilot_files = sorted(pilot_dir.glob('pilot_raw_data_*.json'))
        if pilot_files:
            filepath = pilot_files[-1]
            print(f"Using most recent file: {filepath.name}\n")
        else:
            print("No pilot data files found!")
            sys.exit(1)
    else:
        filepath = Path(sys.argv[1])
    
    summarize_pilot(filepath)