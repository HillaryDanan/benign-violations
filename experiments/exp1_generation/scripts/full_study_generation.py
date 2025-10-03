"""
Full Study: Scaled Humor Generation

Scales pilot to N=300 jokes (75 per category) for statistical power.
Based on pilot findings:
- Use temperature 0.7 (performed well in pilot)
- Focus on GPT-4o and Claude (both 100% success rate)
- Increase jokes per category for robust analysis
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
from datetime import datetime
from tqdm import tqdm

from src import config
from src.llm_interface import LLMInterface
from src.prompt_templates import get_novel_prompts, generate_prompt, NOVEL_CONTEXTS
from src.utils import parse_joke_structure, calculate_joke_metrics, save_joke_data

# Full study parameters
FULL_STUDY_CONFIG = {
    'n_per_category': 75,
    'temperature': 0.7,  # Optimal from pilot
    'models': ['gpt4o', 'claude'],  # Exclude Gemini due to systematic failures
    'categories': ['linguistic', 'physical', 'social', 'dark']
}

def generate_extended_prompts(category: str, n: int) -> list:
    """
    Generate extended prompt list for full study.
    Combines pilot prompts + new variations.
    """
    # Use pilot prompts
    base_contexts = NOVEL_CONTEXTS[category]
    
    # Generate additional contexts if needed
    prompts = []
    for i in range(n):
        context_idx = i % len(base_contexts)
        context = base_contexts[context_idx]
        prompts.append(generate_prompt(category, context))
    
    return prompts

def run_full_study():
    """Execute full study joke generation."""
    
    config_params = FULL_STUDY_CONFIG
    
    print("="*70)
    print(" BENIGN VIOLATIONS: FULL STUDY GENERATION")
    print("="*70)
    
    print(f"\n{'STUDY PARAMETERS':^70}")
    print("-"*70)
    print(f"  Jokes per category: {config_params['n_per_category']}")
    print(f"  Categories: {len(config_params['categories'])}")
    print(f"  Models: {len(config_params['models'])}")
    print(f"  Temperature: {config_params['temperature']} (optimal from pilot)")
    
    total_generations = (
        len(config_params['models']) * 
        len(config_params['categories']) * 
        config_params['n_per_category']
    )
    
    print(f"\n  Total generations: {total_generations}")
    print(f"  Estimated cost: $50-75 USD")
    print(f"  Estimated time: 45-60 minutes")
    
    print("\n" + "="*70)
    
    response = input("\n▶ Press ENTER to start full study generation (or Ctrl+C to cancel): ")
    
    print("\n🔬 Beginning full study generation...\n")
    
    all_results = []
    
    pbar = tqdm(total=total_generations, desc="Generating jokes")
    
    for model_key in config_params['models']:
        llm = LLMInterface(model_key)
        
        for category in config_params['categories']:
            # Get extended prompts
            prompts = generate_extended_prompts(category, config_params['n_per_category'])
            
            for idx, prompt in enumerate(prompts):
                try:
                    response = llm.generate(prompt, temperature=config_params['temperature'])
                    
                    if response.get('text'):
                        parsed = parse_joke_structure(response['text'])
                        metrics = calculate_joke_metrics(parsed)
                    else:
                        parsed = {'setup': '', 'punchline': '', 'full_text': ''}
                        metrics = {}
                    
                    result = {
                        'id': f"{model_key}_{category}_full_{idx}",
                        'timestamp': datetime.now().isoformat(),
                        'model': model_key,
                        'model_name': config.MODELS[model_key]['name'],
                        'category': category,
                        'temperature': config_params['temperature'],
                        'prompt_index': idx,
                        'prompt': prompt,
                        'raw_response': response.get('text', ''),
                        'setup': parsed['setup'],
                        'punchline': parsed['punchline'],
                        'full_text': parsed['full_text'],
                        'metrics': metrics,
                        'api_info': {
                            'tokens': response.get('tokens'),
                            'latency': response.get('latency'),
                            'finish_reason': response.get('finish_reason'),
                            'error': response.get('error')
                        }
                    }
                    
                    all_results.append(result)
                    
                except Exception as e:
                    print(f"\n⚠ Error: {model_key}/{category}/idx={idx}: {str(e)}")
                    
                    all_results.append({
                        'id': f"{model_key}_{category}_full_{idx}",
                        'timestamp': datetime.now().isoformat(),
                        'model': model_key,
                        'category': category,
                        'temperature': config_params['temperature'],
                        'prompt_index': idx,
                        'generation_error': str(e)
                    })
                
                pbar.update(1)
    
    pbar.close()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = config.EXPERIMENTS_DIR / 'exp1_generation' / 'full_study'
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"full_study_data_{timestamp}.json"
    save_joke_data(all_results, output_file)
    
    # Summary
    successful = sum(1 for r in all_results if r.get('raw_response'))
    
    print("\n" + "="*70)
    print(" FULL STUDY GENERATION COMPLETE")
    print("="*70)
    print(f"\nTotal attempts: {len(all_results)}")
    print(f"Successful: {successful} ({100*successful/len(all_results):.1f}%)")
    print(f"\nSaved to: {output_file}")
    print("="*70 + "\n")
    
    return output_file

if __name__ == '__main__':
    try:
        output_file = run_full_study()
        print("\n✓ Ready for full analysis pipeline!")
        print("\nNext steps:")
        print("  1. Run structural analysis")
        print("  2. Run surprise analysis (larger sample)")
        print("  3. Collect explanations (all jokes)")
        print("  4. Manual validation coding")
        print("  5. Statistical inference (mixed-effects models)")
    except KeyboardInterrupt:
        print("\n\n⚠ Generation interrupted. Exiting.")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        raise