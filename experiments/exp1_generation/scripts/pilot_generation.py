"""
Pilot Study: Humor Generation Across Categories

Theoretical Foundation:
    Tests three competing hypotheses about humor generation in LLMs:
    H1 (Semantic Sufficiency): Performance equivalent across all categories
    H2 (Embodied Necessity): Systematic failure across all categories
    H3 (Hybrid Account): Performance ranking: linguistic > social > physical > dark

Design:
    - N=5 jokes per condition (pilot to determine optimal parameters)
    - 4 categories varying in embodiment requirements
    - 3 models (GPT-4o, Claude-3.5-Sonnet, Gemini-2.5-Flash)
    - 3 temperatures (0.5, 0.7, 0.9) to find creativity/coherence optimum
    - Total: 180 generations

Dependent Variables (to be manually rated):
    - Funniness (1-7): Primary outcome measure
    - Category fit (1-7): Manipulation check
    - Structural coherence (1-7): Quality control
    - Originality (1-7): Training data contamination check

Analysis Plan:
    After manual rating, will examine:
    1. Temperature effects (find optimal)
    2. Category × Model interactions (test H3 predictions)
    3. Structural quality by condition
    4. Originality patterns
"""

import sys
from pathlib import Path
# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
from datetime import datetime
from tqdm import tqdm

# Import from src directory
from src import config
from src.llm_interface import LLMInterface
from src.prompt_templates import get_novel_prompts
from src.utils import parse_joke_structure, calculate_joke_metrics, save_joke_data

def run_pilot_generation():
    """Execute pilot study joke generation with full experimental controls."""
    
    print("="*70)
    print(" BENIGN VIOLATIONS: HUMOR GENERATION IN LLMS - PILOT STUDY")
    print("="*70)
    
    print(f"\n{'EXPERIMENTAL DESIGN':^70}")
    print("-"*70)
    print(f"  Models: {list(config.MODELS.keys())}")
    print(f"    - GPT-4o: {config.MODELS['gpt4o']['name']}")
    print(f"    - Claude: {config.MODELS['claude']['name']}")
    print(f"    - Gemini: {config.MODELS['gemini']['name']}")
    print(f"\n  Categories (ordered by embodiment requirement):")
    for i, cat in enumerate(config.HUMOR_CATEGORIES, 1):
        print(f"    {i}. {cat.capitalize()}")
    print(f"\n  Temperatures: {config.PILOT_TEMPERATURES}")
    print(f"    (Testing creativity/coherence trade-off)")
    print(f"\n  Jokes per condition: {config.PILOT_N_PER_CONDITION}")
    
    total_generations = (
        len(config.MODELS) * 
        len(config.HUMOR_CATEGORIES) * 
        len(config.PILOT_TEMPERATURES) * 
        config.PILOT_N_PER_CONDITION
    )
    
    print(f"\n{'PARAMETERS':^70}")
    print("-"*70)
    print(f"  Total generations: {total_generations}")
    print(f"  Estimated cost: $8-12 USD")
    print(f"  Estimated time: 15-20 minutes")
    print(f"  Max tokens per joke: {config.MODELS['gpt4o']['max_tokens']}")
    
    print(f"\n{'HYPOTHESIS TESTING':^70}")
    print("-"*70)
    print(f"  H3 (Hybrid) Prediction: linguistic > social > physical > dark")
    print(f"  Temperature Prediction: 0.7 optimal for surprise/coherence balance")
    print(f"  Novelty Control: Using unusual topic combinations")
    
    print("\n" + "="*70)
    
    response = input("\n▶ Press ENTER to start generation (or Ctrl+C to cancel): ")
    
    print("\n🔬 Beginning systematic joke generation...\n")
    
    all_results = []
    generation_errors = []
    
    # Progress bar
    pbar = tqdm(
        total=total_generations, 
        desc="Generating jokes",
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
    )
    
    # Systematic iteration through all experimental conditions
    for model_key in config.MODELS:
        llm = LLMInterface(model_key)
        
        for category in config.HUMOR_CATEGORIES:
            # Get novel prompts with unusual topic combinations
            # to minimize training data retrieval
            prompts = get_novel_prompts(category, n=config.PILOT_N_PER_CONDITION)
            
            for temp in config.PILOT_TEMPERATURES:
                for idx, prompt in enumerate(prompts):
                    try:
                        # Generate joke via API call
                        response = llm.generate(prompt, temperature=temp)
                        
                        # Parse structural components
                        if response.get('text'):
                            parsed = parse_joke_structure(response['text'])
                            metrics = calculate_joke_metrics(parsed)
                        else:
                            parsed = {
                                'setup': '', 
                                'punchline': '', 
                                'full_text': ''
                            }
                            metrics = {}
                        
                        # Compile complete experimental record
                        result = {
                            # Identifiers
                            'id': f"{model_key}_{category}_t{temp}_{idx}",
                            'timestamp': datetime.now().isoformat(),
                            
                            # Experimental conditions
                            'model': model_key,
                            'model_full_name': config.MODELS[model_key]['name'],
                            'category': category,
                            'temperature': temp,
                            'prompt_index': idx,
                            
                            # Prompts and responses
                            'prompt': prompt,
                            'raw_response': response.get('text', ''),
                            
                            # Parsed joke structure
                            'setup': parsed['setup'],
                            'punchline': parsed['punchline'],
                            'full_text': parsed['full_text'],
                            
                            # Structural metrics
                            'metrics': metrics,
                            
                            # API metadata
                            'api_info': {
                                'tokens': response.get('tokens'),
                                'latency_seconds': response.get('latency'),
                                'finish_reason': response.get('finish_reason'),
                                'error': response.get('error')
                            },
                            
                            # Placeholder for manual ratings (to be added)
                            'manual_ratings': {
                                'funniness': None,
                                'category_fit': None,
                                'structural_coherence': None,
                                'originality': None,
                                'notes': ''
                            }
                        }
                        
                        all_results.append(result)
                        
                    except Exception as e:
                        error_msg = f"{model_key}/{category}/temp={temp}/idx={idx}: {str(e)}"
                        generation_errors.append(error_msg)
                        
                        # Log error but continue with null result
                        all_results.append({
                            'id': f"{model_key}_{category}_t{temp}_{idx}",
                            'timestamp': datetime.now().isoformat(),
                            'model': model_key,
                            'category': category,
                            'temperature': temp,
                            'prompt_index': idx,
                            'generation_error': str(e),
                            'manual_ratings': {
                                'funniness': None,
                                'category_fit': None,
                                'structural_coherence': None,
                                'originality': None,
                                'notes': 'GENERATION FAILED'
                            }
                        })
                    
                    pbar.update(1)
    
    pbar.close()
    
    # Save complete dataset
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = config.PILOT_DIR / f"pilot_raw_data_{timestamp}.json"
    save_joke_data(all_results, output_file)
    
    # Generate summary statistics
    print("\n" + "="*70)
    print(f"{'PILOT GENERATION COMPLETE':^70}")
    print("="*70)
    
    successful = sum(1 for r in all_results if r.get('raw_response'))
    failed = len(all_results) - successful
    
    print(f"\n{'GENERATION STATISTICS':^70}")
    print("-"*70)
    print(f"  Total attempts: {len(all_results)}")
    print(f"  Successful: {successful} ({100*successful/len(all_results):.1f}%)")
    print(f"  Failed: {failed}")
    
    if successful > 0:
        # Calculate descriptive statistics
        total_tokens = sum(
            r['api_info'].get('tokens', 0) 
            for r in all_results 
            if r.get('api_info')
        )
        avg_latency = sum(
            r['api_info'].get('latency_seconds', 0) 
            for r in all_results 
            if r.get('api_info')
        ) / successful
        avg_words = sum(
            r['metrics'].get('total_words', 0) 
            for r in all_results 
            if r.get('metrics')
        ) / successful
        
        print(f"\n  Average joke length: {avg_words:.1f} words")
        print(f"  Average latency: {avg_latency:.2f} seconds")
        print(f"  Total tokens used: {total_tokens:,}")
    
    if generation_errors:
        print(f"\n⚠  ERRORS ENCOUNTERED: {len(generation_errors)}")
        for err in generation_errors[:5]:  # Show first 5
            print(f"    - {err}")
        if len(generation_errors) > 5:
            print(f"    ... and {len(generation_errors)-5} more")
    
    print(f"\n{'OUTPUT':^70}")
    print("-"*70)
    print(f"  Data saved to: {output_file}")
    print(f"  Format: JSON with {len(all_results)} records")
    
    print(f"\n{'NEXT STEPS - MANUAL RATING':^70}")
    print("-"*70)
    print(f"  1. Open: {output_file}")
    print(f"  2. For each joke, rate on 1-7 scale:")
    print(f"     • funniness: How funny is this joke?")
    print(f"     • category_fit: Does it match intended category?")
    print(f"     • structural_coherence: Setup/punchline clear?")
    print(f"     • originality: Novel or seems retrieved?")
    print(f"  3. Add notes for interesting observations")
    print(f"  4. Save as: pilot_rated_data_{timestamp}.json")
    print(f"  5. Run analysis script (coming next)")
    
    print(f"\n{'SCIENTIFIC NOTE':^70}")
    print("-"*70)
    print("  Manual rating by single coder (you) is appropriate for pilot")
    print("  to determine if hypotheses are testable and refine methods.")
    print("  Full study will require multiple blind raters for reliability.")
    
    print("\n" + "="*70)
    print("✓ Pilot generation complete! Ready for manual analysis.")
    print("="*70 + "\n")
    
    return output_file

if __name__ == '__main__':
    try:
        output_file = run_pilot_generation()
    except KeyboardInterrupt:
        print("\n\n⚠ Generation interrupted by user. Exiting gracefully.")
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {str(e)}")
        print("Check API keys and internet connection.")
        raise