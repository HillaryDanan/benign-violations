"""
Semantic Surprise Analysis: Computational Measure of Prediction Error

Tests core humor theory: Jokes should show OPTIMAL surprise.
- Too predictable = boring (no prediction error)
- Too surprising = incoherent (can't resolve)
- Optimal = moderate surprise (prediction error + successful resolution)

Methods:
1. Perplexity: How surprising is punchline given setup?
2. Semantic distance: How far does punchline diverge from setup?
3. Cloze probability: Could you predict the punchline?

Hypothesis: Humor requires MODERATE surprise (U-shaped relationship).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
import pandas as pd
import numpy as np
from tqdm import tqdm

from src.llm_interface import LLMInterface

def calculate_surprise_metrics(setup: str, punchline: str, model_key: str = 'gpt4o') -> dict:
    """
    Calculate computational surprise using LLM.
    
    Uses GPT-4o to measure how surprising the punchline is given the setup.
    """
    llm = LLMInterface(model_key)
    
    # Method 1: Direct completion probability
    # Ask model to complete the setup, see if it matches punchline
    completion_prompt = f"""Given this joke setup, predict what the punchline will be.

Setup: {setup}

What do you predict the punchline is? Give only the punchline, no explanation."""
    
    try:
        response = llm.generate(completion_prompt, temperature=0.7)
        predicted_punchline = response.get('text', '').strip()
        
        # Calculate semantic similarity (crude: word overlap)
        setup_words = set(setup.lower().split())
        punchline_words = set(punchline.lower().split())
        predicted_words = set(predicted_punchline.lower().split())
        
        # Overlap metrics
        punchline_overlap = len(punchline_words & setup_words) / max(len(punchline_words), 1)
        prediction_accuracy = len(predicted_words & punchline_words) / max(len(predicted_words | punchline_words), 1)
        
        return {
            'predicted_punchline': predicted_punchline,
            'punchline_overlap_with_setup': punchline_overlap,
            'prediction_accuracy': prediction_accuracy,
            'surprise_score': 1 - prediction_accuracy,  # Higher = more surprising
            'success': True
        }
    except Exception as e:
        return {
            'predicted_punchline': None,
            'punchline_overlap_with_setup': None,
            'prediction_accuracy': None,
            'surprise_score': None,
            'success': False,
            'error': str(e)
        }

def run_surprise_analysis(input_file: Path, sample_size: int = 30):
    """
    Analyze semantic surprise for a sample of jokes.
    
    Args:
        input_file: Path to pilot data
        sample_size: Number of jokes to analyze (API cost consideration)
    """
    
    print("="*70)
    print(" SEMANTIC SURPRISE ANALYSIS")
    print("="*70)
    print(f"\nNote: Analyzing sample of {sample_size} jokes to minimize API costs")
    print("This tests core prediction error theory of humor.\n")
    
    # Load data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Filter successful jokes with valid structure
    successful = [d for d in data if d.get('raw_response') and 
                 d.get('setup') and d.get('punchline')]
    
    print(f"Total valid jokes: {len(successful)}")
    
    # Sample evenly across categories
    categories = ['linguistic', 'physical', 'social', 'dark']
    per_category = sample_size // 4
    
    sampled = []
    for cat in categories:
        cat_jokes = [j for j in successful if j.get('category') == cat]
        sampled.extend(cat_jokes[:per_category])
    
    print(f"Sampled: {len(sampled)} jokes ({per_category} per category)")
    print("\nCalculating surprise scores (this may take 2-3 minutes)...\n")
    
    results = []
    for joke in tqdm(sampled, desc="Analyzing surprise"):
        surprise_metrics = calculate_surprise_metrics(
            joke['setup'], 
            joke['punchline']
        )
        
        result = {
            'id': joke['id'],
            'model': joke['model'],
            'category': joke['category'],
            'temperature': joke['temperature'],
            'setup': joke['setup'],
            'punchline': joke['punchline'],
            **surprise_metrics
        }
        results.append(result)
    
    df = pd.DataFrame(results)
    successful_analyses = df['success'].sum()
    
    print("\n" + "="*70)
    print(" SURPRISE ANALYSIS RESULTS")
    print("="*70)
    
    print(f"\nSuccessful analyses: {successful_analyses}/{len(df)}")
    
    if successful_analyses > 0:
        valid_df = df[df['success']]
        
        print(f"\n{'OVERALL SURPRISE STATISTICS':^70}")
        print("-"*70)
        print(f"  Mean surprise score: {valid_df['surprise_score'].mean():.3f}")
        print(f"  Std deviation: {valid_df['surprise_score'].std():.3f}")
        print(f"  Range: {valid_df['surprise_score'].min():.3f} - {valid_df['surprise_score'].max():.3f}")
        
        print(f"\n  Mean punchline-setup overlap: {valid_df['punchline_overlap_with_setup'].mean():.3f}")
        print("  (Lower = more novel punchline)")
        
        # By category (H3 test!)
        print(f"\n{'SURPRISE BY CATEGORY (H3 TEST)':^70}")
        print("-"*70)
        print("Hypothesis: Linguistic should show moderate surprise")
        print("Physical/Dark may show higher surprise (harder to predict)\n")
        
        cat_stats = valid_df.groupby('category').agg({
            'surprise_score': ['mean', 'std', 'count']
        }).round(3)
        print(cat_stats.to_string())
        
        # By model
        print(f"\n{'SURPRISE BY MODEL':^70}")
        print("-"*70)
        model_stats = valid_df.groupby('model').agg({
            'surprise_score': ['mean', 'std', 'count']
        }).round(3)
        print(model_stats.to_string())
    
    # Save results
    output_file = input_file.parent / 'surprise_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    df.to_csv(input_file.parent / 'surprise_analysis.csv', index=False)
    
    print(f"\n✓ Surprise analysis complete!")
    print(f"  Saved to: {output_file}")
    print("="*70 + "\n")
    
    return df

if __name__ == '__main__':
    import sys
    
    pilot_dir = Path(__file__).parent.parent / 'pilot'
    pilot_files = sorted(pilot_dir.glob('pilot_raw_data_*.json'))
    
    if not pilot_files:
        print("Error: No pilot data found!")
        sys.exit(1)
    
    input_file = pilot_files[-1]
    print(f"Using: {input_file.name}\n")
    
    # Allow custom sample size
    sample_size = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    
    run_surprise_analysis(input_file, sample_size=sample_size)