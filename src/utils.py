"""
Utility functions for the Benign Violations project.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import re
import time
from typing import Dict, List
import requests

def parse_joke_structure(text: str) -> Dict[str, str]:
    """
    Parse joke into setup and punchline components.
    
    Args:
        text: Raw joke text from LLM
        
    Returns:
        Dictionary with 'setup', 'punchline', 'full_text'
    """
    # Try to find explicit Setup/Punchline markers
    setup_match = re.search(r'Setup:\s*(.+?)(?=Punchline:|$)', text, re.IGNORECASE | re.DOTALL)
    punchline_match = re.search(r'Punchline:\s*(.+?)$', text, re.IGNORECASE | re.DOTALL)
    
    if setup_match and punchline_match:
        setup = setup_match.group(1).strip()
        punchline = punchline_match.group(1).strip()
    else:
        # If no markers, split on common patterns
        # Try question/answer format
        if '?' in text:
            parts = text.split('?', 1)
            setup = parts[0].strip() + '?'
            punchline = parts[1].strip() if len(parts) > 1 else ''
        else:
            # Default: split on sentence boundaries, last sentence is punchline
            sentences = re.split(r'[.!]\s+', text)
            if len(sentences) > 1:
                setup = '. '.join(sentences[:-1]) + '.'
                punchline = sentences[-1]
            else:
                setup = text
                punchline = ''
    
    return {
        'setup': setup,
        'punchline': punchline,
        'full_text': text
    }

def check_originality(joke_text: str, max_checks: int = 3) -> Dict[str, any]:
    """
    Check if joke appears online (potential training data contamination).
    
    Uses web search to find exact or near-exact matches.
    
    Args:
        joke_text: The joke to check
        max_checks: Maximum number of search queries
        
    Returns:
        Dictionary with 'is_likely_original', 'matches_found', 'confidence'
    """
    # Note: This is a simplified check. Full implementation would need
    # the web_search tool which isn't available in this context.
    # For pilot, we'll do manual checking.
    
    # Extract key phrases (5+ words) for searching
    words = joke_text.split()
    if len(words) < 5:
        return {
            'is_likely_original': True,
            'matches_found': 0,
            'confidence': 'low',
            'note': 'Joke too short for reliable check'
        }
    
    # For now, return placeholder
    # In full implementation, would search for exact phrases
    return {
        'is_likely_original': None,
        'matches_found': None,
        'confidence': 'manual_check_required',
        'note': 'Automated originality checking requires web search tool'
    }

def calculate_joke_metrics(joke: Dict) -> Dict[str, float]:
    """
    Calculate basic structural metrics for a joke.
    
    Args:
        joke: Parsed joke dictionary
        
    Returns:
        Metrics dictionary
    """
    setup = joke.get('setup', '')
    punchline = joke.get('punchline', '')
    full_text = joke.get('full_text', '')
    
    return {
        'total_words': len(full_text.split()),
        'setup_words': len(setup.split()),
        'punchline_words': len(punchline.split()),
        'setup_to_punchline_ratio': len(setup.split()) / max(len(punchline.split()), 1),
        'has_question': '?' in setup,
        'has_punctuation_emphasis': bool(re.search(r'[!]', punchline))
    }

def save_joke_data(jokes: List[Dict], filename: str):
    """Save jokes to JSON with proper formatting."""
    import json
    from pathlib import Path
    
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(jokes, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(jokes)} jokes to {filename}")

# Test
if __name__ == '__main__':
    test_joke = """Setup: Why don't scientists trust atoms?
    Punchline: Because they make up everything."""
    
    parsed = parse_joke_structure(test_joke)
    print("Parsed joke:")
    print(f"  Setup: {parsed['setup']}")
    print(f"  Punchline: {parsed['punchline']}")
    
    metrics = calculate_joke_metrics(parsed)
    print(f"\nMetrics: {metrics}")