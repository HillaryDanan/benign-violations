"""
Explanation Analysis: Feature Coding

Codes model explanations for presence of:
1. SEMANTIC features: ambiguity, wordplay, incongruity, frame-shifting
2. EMBODIED features: physical consequences, pain, collision, bodily experience
3. SOCIAL features: norm violations, perspective-taking, embarrassment

KEY H3 TEST:
If embodiment is necessary for embodied humor, models should:
- Successfully cite semantic features for linguistic jokes
- FAIL to cite (or incorrectly cite) embodied features for physical jokes
- FAIL to cite (or incorrectly cite) social features for social jokes
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
import pandas as pd
import re
from collections import Counter

# Feature detection keywords
FEATURE_KEYWORDS = {
    'semantic': [
        'ambiguous', 'ambiguity', 'double meaning', 'wordplay', 'pun',
        'multiple meanings', 'semantic', 'reinterpret', 'frame', 'shift',
        'incongruity', 'incongruous', 'unexpected', 'twist', 'surprise'
    ],
    'embodied': [
        'physical', 'pain', 'hurt', 'collision', 'impact', 'body',
        'bodily', 'injury', 'clumsy', 'fall', 'bump', 'hit',
        'sensory', 'tactile', 'kinesthetic', 'motor'
    ],
    'social': [
        'social', 'norm', 'awkward', 'embarrass', 'inappropriate',
        'expect', 'convention', 'etiquette', 'perspective',
        'understand', 'recognize', 'aware', 'context', 'situation'
    ],
    'threat': [
        'threat', 'danger', 'risk', 'harm', 'safe', 'benign',
        'mortality', 'death', 'die', 'kill', 'taboo', 'dark'
    ]
}

def code_explanation(explanation_text: str) -> dict:
    """
    Code explanation for presence of feature types.
    
    Returns:
        Dictionary with binary features and keyword counts
    """
    if not explanation_text:
        return {
            'has_semantic': False,
            'has_embodied': False,
            'has_social': False,
            'has_threat': False,
            'semantic_count': 0,
            'embodied_count': 0,
            'social_count': 0,
            'threat_count': 0
        }
    
    text_lower = explanation_text.lower()
    
    counts = {}
    for feature_type, keywords in FEATURE_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        counts[f'{feature_type}_count'] = count
        counts[f'has_{feature_type}'] = count > 0
    
    return counts

def analyze_explanations(input_file: Path):
    """Analyze coded explanations by category."""
    
    print("="*70)
    print(" EXPLANATION FEATURE ANALYSIS")
    print("="*70)
    
    # Load explanations
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    print(f"\nAnalyzing {len(data)} explanations...")
    
    # Code each explanation
    results = []
    for item in data:
        if not item.get('success'):
            continue
        
        codes = code_explanation(item.get('explanation', ''))
        
        result = {
            'joke_id': item['joke_id'],
            'joke_category': item['joke_category'],
            'joke_generator': item['joke_generator_model'],
            'explaining_model': item['explaining_model'],
            **codes
        }
        results.append(result)
    
    df = pd.DataFrame(results)
    
    # Analysis by category (KEY H3 TEST!)
    print(f"\n{'H3 TEST: FEATURE CITATIONS BY JOKE CATEGORY':^70}")
    print("="*70)
    print("\nHypothesis predictions:")
    print("  Linguistic jokes → High semantic citations")
    print("  Physical jokes → Low embodied citations (if embodiment needed)")
    print("  Social jokes → Low social citations (if social cognition needed)")
    print("  Dark jokes → Low threat citations (if threat assessment needed)\n")
    
    # Calculate proportion citing each feature type by category
    print("-"*70)
    print("PROPORTION OF EXPLANATIONS CITING EACH FEATURE TYPE:")
    print("-"*70)
    
    for category in ['linguistic', 'physical', 'social', 'dark']:
        cat_df = df[df['joke_category'] == category]
        if len(cat_df) == 0:
            continue
        
        print(f"\n{category.upper()} JOKES (n={len(cat_df)}):")
        print(f"  Semantic features: {cat_df['has_semantic'].mean():.2%}")
        print(f"  Embodied features: {cat_df['has_embodied'].mean():.2%}")
        print(f"  Social features: {cat_df['has_social'].mean():.2%}")
        print(f"  Threat features: {cat_df['has_threat'].mean():.2%}")
        
        # Mean keyword counts
        print(f"  Mean semantic keywords: {cat_df['semantic_count'].mean():.2f}")
        print(f"  Mean embodied keywords: {cat_df['embodied_count'].mean():.2f}")
        print(f"  Mean social keywords: {cat_df['social_count'].mean():.2f}")
        print(f"  Mean threat keywords: {cat_df['threat_count'].mean():.2f}")
    
    # By explaining model
    print(f"\n{'FEATURE CITATIONS BY EXPLAINING MODEL':^70}")
    print("-"*70)
    
    model_stats = df.groupby('explaining_model').agg({
        'has_semantic': 'mean',
        'has_embodied': 'mean',
        'has_social': 'mean',
        'has_threat': 'mean'
    }).round(3)
    print(model_stats.to_string())
    
    # Critical comparisons for H3
    print(f"\n{'CRITICAL H3 COMPARISONS':^70}")
    print("="*70)
    
    # Do physical jokes get embodied explanations?
    physical = df[df['joke_category'] == 'physical']
    if len(physical) > 0:
        embodied_rate = physical['has_embodied'].mean()
        print(f"\nPhysical jokes citing embodied features: {embodied_rate:.1%}")
        if embodied_rate < 0.5:
            print("  → SUPPORTS H3: Models fail to cite embodied features!")
        else:
            print("  → Does not support H3: Models cite embodied features")
    
    # Do linguistic jokes get semantic explanations?
    linguistic = df[df['joke_category'] == 'linguistic']
    if len(linguistic) > 0:
        semantic_rate = linguistic['has_semantic'].mean()
        print(f"\nLinguistic jokes citing semantic features: {semantic_rate:.1%}")
        if semantic_rate > 0.7:
            print("  → SUPPORTS H3: Models successfully explain linguistic humor!")
        else:
            print("  → Does not support H3: Models struggle with semantic features")
    
    # Save results
    output_file = input_file.parent / 'explanation_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    df.to_csv(input_file.parent / 'explanation_analysis.csv', index=False)
    
    print(f"\n✓ Analysis complete!")
    print(f"  Saved to: {output_file}")
    print("="*70 + "\n")
    
    return df

if __name__ == '__main__':
    import sys
    
    # Find most recent explanation file
    output_dir = Path(__file__).parent.parent / 'outputs'
    explanation_files = sorted(output_dir.glob('explanations_*.json'))
    
    if not explanation_files:
        print("Error: No explanation data found!")
        print("Run collect_explanations.py first.")
        sys.exit(1)
    
    input_file = explanation_files[-1]
    print(f"Using: {input_file.name}\n")
    
    analyze_explanations(input_file)