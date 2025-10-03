"""
Configuration for Benign Violations experiments.
Handles API keys, model settings, and experimental parameters.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Model configurations
MODELS = {
    'gpt4o': {
        'name': 'gpt-4o',
        'provider': 'openai',
        'max_tokens': 150,
        'description': 'GPT-4o (October 2024)'
    },
    'claude': {
        'name': 'claude-3-5-sonnet-20241022',
        'provider': 'anthropic',
        'max_tokens': 150,
        'description': 'Claude 3.5 Sonnet'
    },
    'gemini': {
        'name': 'gemini-2.0-flash-exp',
        'provider': 'google',
        'max_tokens': 150,
        'description': 'Gemini 2.5 Flash'
    }
}

# Experimental parameters
HUMOR_CATEGORIES = ['linguistic', 'physical', 'social', 'dark']
PILOT_TEMPERATURES = [0.5, 0.7, 0.9]
PILOT_N_PER_CONDITION = 5

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
EXPERIMENTS_DIR = PROJECT_ROOT / 'experiments'
PROMPTS_DIR = EXPERIMENTS_DIR / 'exp1_generation' / 'prompts'
OUTPUTS_DIR = EXPERIMENTS_DIR / 'exp1_generation' / 'outputs'
PILOT_DIR = EXPERIMENTS_DIR / 'exp1_generation' / 'pilot'

# Create directories if they don't exist
for dir_path in [DATA_DIR, OUTPUTS_DIR, PILOT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Validation
def validate_api_keys():
    """Ensure all API keys are present."""
    missing = []
    if not OPENAI_API_KEY:
        missing.append('OPENAI_API_KEY')
    if not ANTHROPIC_API_KEY:
        missing.append('ANTHROPIC_API_KEY')
    if not GOOGLE_API_KEY:
        missing.append('GOOGLE_API_KEY')
    
    if missing:
        raise ValueError(f"Missing API keys: {', '.join(missing)}")
    
    print("✓ All API keys loaded successfully")

if __name__ == '__main__':
    validate_api_keys()