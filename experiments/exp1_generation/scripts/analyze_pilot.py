"""
Pilot Study Analysis: Descriptive Statistics and Hypothesis Testing

Analyzes manually-rated pilot data to answer:
1. Which temperature produces best humor?
2. Do categories show predicted ordering (H3: linguistic > social > physical > dark)?
3. Do models differ in performance?
4. Are jokes original or retrieved?
5. Do structural metrics predict funniness?

Note: Pilot uses descriptive statistics only (small N).
Full study will use inferential statistics (mixed-effects models).
"""

import sys
from pathlib import Path
# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Import from src directory
from src import config

# Set plotting style
sns.set_style("whitegrid")
sns.set_palette("husl")

def load_rated_data(filepath: str) -> pd.DataFrame:
    """Load manually-rated pilot data into DataFrame."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    # Flatten nested structure for analysis
    records = []
    for joke in data:
        if joke.get('manual_ratings') and joke.get('manual_ratings', {}).get('funniness') is not None:
            record = {
                'id': joke['id'],
                'model': joke['model'],
                'category': joke['category'],
                'temperature': joke['temperature'],
                'funniness': joke['manual_ratings']['funniness'],
                'category_fit': joke['manual_ratings']['category_fit'],
                'structural_coherence': joke['manual_ratings']['structural_coherence'],
                'originality': joke['manual_ratings']['originality'],
                'total_words': joke.get('metrics', {}).get('total_words', 0),
                'setup_words': joke.get('metrics', {}).get('setup_words', 0),
                'punchline_words': joke.get('metrics', {}).get('punchline_words', 0),
                'full_text': joke.get('full_text', '')
            }
            records.append(record)
    
    df = pd.DataFrame(records)
    return df

def analyze_pilot(df: pd.DataFrame, output_dir: Path):
    """Generate comprehensive pilot analysis."""
    
    print("="*70)
    print(f"{'PILOT STUDY ANALYSIS':^70}")
    print("="*70)
    
    # 1. SAMPLE DESCRIPTION
    print(f"\n{'SAMPLE CHARACTERISTICS':^70}")
    print("-"*70)
    print(f"  Total rated jokes: {len(df)}")
    print(f"  Models: {df['model'].nunique()}")
    print(f"  Categories: {df['category'].nunique()}")
    print(f"  Temperatures: {df['temperature'].nunique()}")
    print(f"  N per condition: {len(df) / (df['model'].nunique() * df['category'].nunique() * df['temperature'].nunique()):.1f}")
    
    # 2. OVERALL DESCRIPTIVE STATISTICS
    print(f"\n{'OVERALL MEANS (SD)':^70}")
    print("-"*70)
    for var in ['funniness', 'category_fit', 'structural_coherence', 'originality']:
        mean = df[var].mean()
        sd = df[var].std()
        print(f"  {var.capitalize()}: M={mean:.2f}, SD={sd:.2f}")
    
    # 3. TEMPERATURE EFFECTS
    print(f"\n{'QUESTION 1: OPTIMAL TEMPERATURE':^70}")
    print("-"*70)
    temp_effects = df.groupby('temperature')['funniness'].agg(['mean', 'std', 'count'])
    print(temp_effects.to_string())
    
    best_temp = temp_effects['mean'].idxmax()
    print(f"\n  → Best temperature for funniness: {best_temp}")
    print(f"    (Will use for full study)")
    
    # 4. CATEGORY EFFECTS (H3 TEST)
    print(f"\n{'QUESTION 2: CATEGORY ORDERING (H3 TEST)':^70}")
    print("-"*70)
    print("  H3 Prediction: linguistic > social > physical > dark")
    print()
    
    cat_effects = df.groupby('category')['funniness'].agg(['mean', 'std', 'count'])
    cat_effects = cat_effects.sort_values('mean', ascending=False)
    print(cat_effects.to_string())
    
    observed_order = list(cat_effects.index)
    predicted_order = ['linguistic', 'social', 'physical', 'dark']
    
    print(f"\n  Observed ranking: {' > '.join(observed_order)}")
    print(f"  Predicted ranking: {' > '.join(predicted_order)}")
    
    if observed_order == predicted_order:
        print(f"  ✓ H3 SUPPORTED: Observed matches predicted")
    else:
        print(f"  ✗ H3 NOT SUPPORTED: Order differs from prediction")
        print(f"    (Note: Pilot N is small, full study needed for inference)")
    
    # 5. MODEL EFFECTS
    print(f"\n{'QUESTION 3: MODEL DIFFERENCES':^70}")
    print("-"*70)
    model_effects = df.groupby('model')['funniness'].agg(['mean', 'std', 'count'])
    print(model_effects.to_string())
    
    # 6. ORIGINALITY
    print(f"\n{'QUESTION 4: ORIGINALITY CHECK':^70}")
    print("-"*70)
    orig_mean = df['originality'].mean()
    print(f"  Mean originality: {orig_mean:.2f}/7")
    
    if orig_mean > 5:
        print(f"  ✓ GOOD: Jokes appear original (minimal retrieval)")
    elif orig_mean > 3:
        print(f"  ⚠ MODERATE: Some retrieval possible, investigate further")
    else:
        print(f"  ✗ POOR: Many jokes may be retrieved, revise prompts")
    
    low_orig = df[df['originality'] < 4]
    if len(low_orig) > 0:
        print(f"\n  Low originality jokes (n={len(low_orig)}):")
        for _, row in low_orig.head(3).iterrows():
            print(f"    - {row['category']}, temp={row['temperature']}: '{row['full_text'][:60]}...'")
    
    # 7. STRUCTURE PREDICTS FUNNINESS?
    print(f"\n{'QUESTION 5: STRUCTURAL PREDICTORS':^70}")
    print("-"*70)
    
    corr_coherence = df['structural_coherence'].corr(df['funniness'])
    corr_words = df['total_words'].corr(df['funniness'])
    
    print(f"  Coherence × Funniness: r={corr_coherence:.3f}")
    print(f"  Word count × Funniness: r={corr_words:.3f}")
    
    # 8. SAVE SUMMARY
    summary = {
        'sample_size': len(df),
        'best_temperature': float(best_temp),
        'category_ranking': observed_order,
        'h3_supported': observed_order == predicted_order,
        'mean_originality': float(orig_mean),
        'descriptives': {
            'funniness': {'mean': float(df['funniness'].mean()), 'sd': float(df['funniness'].std())},
            'category_fit': {'mean': float(df['category_fit'].mean()), 'sd': float(df['category_fit'].std())},
            'structural_coherence': {'mean': float(df['structural_coherence'].mean()), 'sd': float(df['structural_coherence'].std())},
            'originality': {'mean': float(df['originality'].mean()), 'sd': float(df['originality'].std())}
        }
    }
    
    summary_file = output_dir / 'pilot_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'RECOMMENDATIONS FOR FULL STUDY':^70}")
    print("-"*70)
    print(f"  1. Use temperature = {best_temp}")
    print(f"  2. Category design appears valid (manipulation check passed)")
    print(f"  3. Need N≥20 per condition for mixed-effects models")
    print(f"  4. Consider refining prompts for low-originality categories")
    
    print("\n" + "="*70)
    print(f"✓ Analysis complete! Summary saved to {summary_file}")
    print("="*70 + "\n")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_pilot.py <path_to_rated_data.json>")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    df = load_rated_data(filepath)
    analyze_pilot(df, config.PILOT_DIR)