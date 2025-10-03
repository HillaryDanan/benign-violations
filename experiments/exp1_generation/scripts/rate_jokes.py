"""
Interactive joke rating interface.

Presents jokes one at a time for manual rating.
Saves progress after each rating (safe against interruption).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
from datetime import datetime

def clear_screen():
    """Clear terminal screen."""
    print("\n" * 50)

def display_joke(joke, index, total):
    """Display single joke with context."""
    clear_screen()
    
    print("="*70)
    print(f" JOKE {index}/{total}")
    print("="*70)
    
    print(f"\nModel: {joke.get('model', 'N/A')}")
    print(f"Category: {joke.get('category', 'N/A')}")
    print(f"Temperature: {joke.get('temperature', 'N/A')}")
    
    print("\n" + "-"*70)
    print("JOKE:")
    print("-"*70)
    print(f"\n{joke.get('full_text', 'N/A')}\n")
    print("-"*70)

def get_rating(dimension, scale="1-7"):
    """Get rating with validation."""
    while True:
        try:
            response = input(f"\n{dimension} ({scale}): ").strip()
            
            # Allow skip
            if response.lower() in ['s', 'skip']:
                return None
            
            # Allow quit
            if response.lower() in ['q', 'quit']:
                return 'QUIT'
            
            rating = int(response)
            if 1 <= rating <= 7:
                return rating
            else:
                print("  ⚠ Please enter a number between 1 and 7")
        except ValueError:
            print("  ⚠ Please enter a valid number (or 's' to skip, 'q' to quit)")

def rate_jokes(input_file: Path):
    """Interactive rating session."""
    
    # Load data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Filter to successful jokes only
    successful_jokes = [d for d in data if d.get('raw_response')]
    
    # Check for existing ratings
    already_rated = sum(1 for j in successful_jokes 
                       if j.get('manual_ratings', {}).get('funniness') is not None)
    
    print("="*70)
    print(" BENIGN VIOLATIONS: JOKE RATING INTERFACE")
    print("="*70)
    print(f"\nTotal successful jokes: {len(successful_jokes)}")
    print(f"Already rated: {already_rated}")
    print(f"Remaining: {len(successful_jokes) - already_rated}")
    
    print("\n" + "="*70)
    print(" RATING INSTRUCTIONS")
    print("="*70)
    print("\nFor each joke, rate on a 1-7 scale:")
    print("\n  1. FUNNINESS: How funny is this joke?")
    print("     1=Not funny at all → 7=Extremely funny")
    print("\n  2. CATEGORY FIT: Does it match the intended category?")
    print("     1=Completely wrong category → 7=Perfect category match")
    print("\n  3. STRUCTURAL COHERENCE: Is the setup/punchline clear?")
    print("     1=Incoherent/confusing → 7=Perfectly structured")
    print("\n  4. ORIGINALITY: Does this seem novel or retrieved?")
    print("     1=Clearly copied/cliché → 7=Highly original")
    
    print("\nCommands:")
    print("  • Enter 1-7 for rating")
    print("  • Type 's' or 'skip' to skip this joke")
    print("  • Type 'q' or 'quit' to save and exit")
    
    input("\nPress ENTER to begin rating...")
    
    # Rating loop
    total = len(successful_jokes)
    rated_count = 0
    
    for idx, joke in enumerate(successful_jokes, 1):
        # Skip if already rated
        if joke.get('manual_ratings', {}).get('funniness') is not None:
            continue
        
        # Display joke
        display_joke(joke, idx, total)
        
        # Get ratings
        print("\nRATE THIS JOKE:")
        
        funniness = get_rating("Funniness")
        if funniness == 'QUIT':
            break
        
        category_fit = get_rating("Category fit")
        if category_fit == 'QUIT':
            break
        
        coherence = get_rating("Structural coherence")
        if coherence == 'QUIT':
            break
        
        originality = get_rating("Originality")
        if originality == 'QUIT':
            break
        
        # Get notes
        notes = input("\nNotes (optional, press ENTER to skip): ").strip()
        
        # Save ratings
        joke['manual_ratings'] = {
            'funniness': funniness,
            'category_fit': category_fit,
            'structural_coherence': coherence,
            'originality': originality,
            'notes': notes,
            'rated_at': datetime.now().isoformat()
        }
        
        rated_count += 1
        
        # Save progress after each rating (safety!)
        with open(input_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✓ Saved! ({rated_count} rated this session)")
    
    # Final save and summary
    with open(input_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    clear_screen()
    print("="*70)
    print(" RATING SESSION COMPLETE")
    print("="*70)
    print(f"\nJokes rated this session: {rated_count}")
    
    total_rated = sum(1 for j in successful_jokes 
                     if j.get('manual_ratings', {}).get('funniness') is not None)
    print(f"Total jokes now rated: {total_rated}/{len(successful_jokes)}")
    
    if total_rated == len(successful_jokes):
        print("\n🎉 ALL JOKES RATED! Ready for analysis!")
        
        # Create rated data file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = input_file.parent / f"pilot_rated_data_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✓ Saved complete rated dataset to:")
        print(f"  {output_file}")
        
        print("\n" + "="*70)
        print(" NEXT STEP: RUN ANALYSIS")
        print("="*70)
        print(f"\npython3 experiments/exp1_generation/scripts/analyze_pilot.py \\")
        print(f"  {output_file}")
    else:
        remaining = len(successful_jokes) - total_rated
        print(f"\nRemaining jokes to rate: {remaining}")
        print("\nRun this script again to continue rating.")
    
    print("\n" + "="*70)

if __name__ == '__main__':
    # Find most recent pilot file
    pilot_dir = Path(__file__).parent.parent / 'pilot'
    pilot_files = sorted(pilot_dir.glob('pilot_raw_data_*.json'))
    
    if not pilot_files:
        print("Error: No pilot data files found!")
        sys.exit(1)
    
    input_file = pilot_files[-1]
    print(f"\nUsing file: {input_file.name}")
    
    rate_jokes(input_file)