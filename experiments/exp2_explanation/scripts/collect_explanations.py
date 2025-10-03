"""
Explanation Collection: Why is this funny?

Core H3 test: Do LLM explanations differ by joke category?

Prediction (Hybrid Hypothesis):
- Linguistic jokes → Models cite semantic features (ambiguity, wordplay)
- Physical jokes → Models FAIL to cite embodied features (pain, collision)
- Dark jokes → Models FAIL to cite threat assessment

This tests whether models understand the mechanisms behind different humor types.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
from datetime import datetime
from tqdm import tqdm

from src import config
from src.llm_interface import LLMInterface

EXPLANATION_PROMPT = """You are analyzing humor for a cognitive science study.

Below is a joke. Please explain why this joke is intended to be funny. Focus on the MECHANISMS that create humor.

Joke:
{full_text}

Explain why this is funny. Consider:
- What expectations does the setup create?
- How does the punchline violate those expectations?
- What knowledge is required to understand the joke?
- What makes the violation "benign" (safe, acceptable)?

Provide a detailed analysis in 3-5 sentences."""

def collect_explanation(joke: dict, model_key: str) -> dict:
    """Get model's explanation of why a joke is funny."""
    
    llm = LLMInterface(model_key)
    
    prompt = EXPLANATION_PROMPT.format(full_text=joke['full_text'])
    
    try:
        response = llm.generate(prompt, temperature=0.3)  # Lower temp for analytical task
        
        return {
            'joke_id': joke['id'],
            'explaining_model': model_key,
            'explanation': response.get('text', ''),
            'success': True,
            'tokens': response.get('tokens'),
            'latency': response.get('latency')
        }
    except Exception as e:
        return {
            'joke_id': joke['id'],
            'explaining_model': model_key,
            'explanation': None,
            'success': False,
            'error': str(e)
        }

def run_explanation_collection(input_file: Path, 
                               explaining_models: list = None,
                               sample_size: int = None):
    """
    Collect explanations from models about why jokes are funny.
    
    Args:
        input_file: Pilot data file
        explaining_models: Which models to use for explanations (default: all 3)
        sample_size: How many jokes to explain (default: all successful)
    """
    
    if explaining_models is None:
        explaining_models = ['gpt4o', 'claude', 'gemini']
    
    print("="*70)
    print(" EXPLANATION COLLECTION: WHY IS THIS FUNNY?")
    print("="*70)
    print(f"\nExplaining models: {explaining_models}")
    
    # Load data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Filter successful jokes with valid structure
    successful = [d for d in data if d.get('raw_response') and 
                 d.get('full_text')]
    
    if sample_size:
        # Sample evenly across categories
        categories = ['linguistic', 'physical', 'social', 'dark']
        per_category = sample_size // 4
        sampled = []
        for cat in categories:
            cat_jokes = [j for j in successful if j.get('category') == cat]
            sampled.extend(cat_jokes[:per_category])
        jokes_to_explain = sampled
    else:
        jokes_to_explain = successful
    
    print(f"Jokes to explain: {len(jokes_to_explain)}")
    print(f"Total explanations to collect: {len(jokes_to_explain) * len(explaining_models)}")
    print(f"\nEstimated time: 5-10 minutes")
    print(f"Estimated cost: $5-10\n")
    
    input("Press ENTER to begin explanation collection...")
    
    all_explanations = []
    
    total_calls = len(jokes_to_explain) * len(explaining_models)
    pbar = tqdm(total=total_calls, desc="Collecting explanations")
    
    for joke in jokes_to_explain:
        for model_key in explaining_models:
            explanation_data = collect_explanation(joke, model_key)
            
            # Add joke metadata
            explanation_data.update({
                'joke_category': joke['category'],
                'joke_generator_model': joke['model'],
                'joke_temperature': joke['temperature'],
                'timestamp': datetime.now().isoformat()
            })
            
            all_explanations.append(explanation_data)
            pbar.update(1)
    
    pbar.close()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(__file__).parent.parent / 'outputs'
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f'explanations_{timestamp}.json'
    
    with open(output_file, 'w') as f:
        json.dump(all_explanations, f, indent=2)
    
    # Summary
    successful_explanations = sum(1 for e in all_explanations if e['success'])
    
    print("\n" + "="*70)
    print(" EXPLANATION COLLECTION COMPLETE")
    print("="*70)
    print(f"\nTotal explanations collected: {len(all_explanations)}")
    print(f"Successful: {successful_explanations}")
    print(f"Failed: {len(all_explanations) - successful_explanations}")
    
    print(f"\n✓ Saved to: {output_file}")
    
    print(f"\n{'NEXT STEP: CODE EXPLANATIONS':^70}")
    print("-"*70)
    print("Run explanation analyzer to code for feature types:")
    print(f"  python3 experiments/exp2_explanation/scripts/analyze_explanations.py")
    
    print("="*70 + "\n")
    
    return output_file

if __name__ == '__main__':
    import sys
    
    pilot_dir = Path(__file__).parent.parent.parent / 'exp1_generation' / 'pilot'
    pilot_files = sorted(pilot_dir.glob('pilot_raw_data_*.json'))
    
    if not pilot_files:
        print("Error: No pilot data found!")
        sys.exit(1)
    
    input_file = pilot_files[-1]
    print(f"Using: {input_file.name}\n")
    
    # Default: Explain 40 jokes (10 per category) with all 3 models = 120 explanations
    sample_size = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    
    run_explanation_collection(input_file, sample_size=sample_size)