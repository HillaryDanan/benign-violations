"""
Full Study: Comprehensive Explanation Collection

Collects explanations for all generated jokes from all models.
Enables robust statistical analysis and manual validation.
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

def collect_full_study_explanations(input_file: Path, explaining_models: list = None):
    """Collect explanations for full study."""
    
    if explaining_models is None:
        explaining_models = ['gpt4o', 'claude', 'gemini']
    
    print("="*70)
    print(" FULL STUDY: EXPLANATION COLLECTION")
    print("="*70)
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    successful = [d for d in data if d.get('raw_response') and d.get('full_text')]
    
    print(f"\nJokes to explain: {len(successful)}")
    print(f"Explaining models: {len(explaining_models)}")
    print(f"Total explanations: {len(successful) * len(explaining_models)}")
    print(f"\nEstimated cost: $75-100 USD")
    print(f"Estimated time: 30-45 minutes\n")
    
    input("Press ENTER to begin...")
    
    all_explanations = []
    total = len(successful) * len(explaining_models)
    
    pbar = tqdm(total=total, desc="Collecting explanations")
    
    for joke in successful:
        for model_key in explaining_models:
            llm = LLMInterface(model_key)
            prompt = EXPLANATION_PROMPT.format(full_text=joke['full_text'])
            
            try:
                response = llm.generate(prompt, temperature=0.3)
                
                explanation_data = {
                    'joke_id': joke['id'],
                    'explaining_model': model_key,
                    'explanation': response.get('text', ''),
                    'success': True,
                    'tokens': response.get('tokens'),
                    'latency': response.get('latency'),
                    'joke_category': joke['category'],
                    'joke_generator_model': joke['model'],
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                explanation_data = {
                    'joke_id': joke['id'],
                    'explaining_model': model_key,
                    'explanation': None,
                    'success': False,
                    'error': str(e),
                    'joke_category': joke['category'],
                    'joke_generator_model': joke['model'],
                    'timestamp': datetime.now().isoformat()
                }
            
            all_explanations.append(explanation_data)
            pbar.update(1)
    
    pbar.close()
    
    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(__file__).parent.parent / 'outputs'
    output_file = output_dir / f'full_study_explanations_{timestamp}.json'
    
    with open(output_file, 'w') as f:
        json.dump(all_explanations, f, indent=2)
    
    successful_expl = sum(1 for e in all_explanations if e['success'])
    
    print("\n" + "="*70)
    print(" EXPLANATION COLLECTION COMPLETE")
    print("="*70)
    print(f"\nTotal: {len(all_explanations)}")
    print(f"Successful: {successful_expl}")
    print(f"\nSaved to: {output_file}")
    print("="*70 + "\n")
    
    return output_file

if __name__ == '__main__':
    # Find most recent full study data
    full_study_dir = Path(__file__).parent.parent.parent / 'exp1_generation' / 'full_study'
    
    if not full_study_dir.exists():
        print("Error: Run full_study_generation.py first!")
        sys.exit(1)
    
    data_files = sorted(full_study_dir.glob('full_study_data_*.json'))
    
    if not data_files:
        print("Error: No full study data found!")
        sys.exit(1)
    
    input_file = data_files[-1]
    print(f"Using: {input_file.name}\n")
    
    collect_full_study_explanations(input_file)