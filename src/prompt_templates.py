"""
Prompt templates for humor generation across categories.

Design principles:
1. Clear category specification to reduce ambiguity
2. Request for novel content to minimize retrieval
3. Structural constraints (setup/punchline) for consistency
4. Explicit word limits to control generation length
"""

# Base template structure
BASE_TEMPLATE = """You are a humor researcher generating jokes for a scientific study.

Task: Create a {category} joke that is:
- Original and novel (not a well-known joke)
- Has clear setup and punchline structure
- Appropriate for academic research
- Between 15-50 words total

Category: {category_description}

Generate exactly ONE joke. Use this format:
Setup: [your setup here]
Punchline: [your punchline here]

Remember: The joke should be {category_specific_instruction}"""

# Category-specific descriptions and instructions
CATEGORY_SPECS = {
    'linguistic': {
        'description': 'Linguistic humor relies on wordplay, puns, homonyms, semantic ambiguity, or double meanings. The humor emerges from language structure itself, not physical actions or social situations.',
        'instruction': 'based purely on word meaning, sound, or semantic ambiguity. Avoid references to physical actions or social situations.',
        'example_topics': ['abstract concepts', 'language itself', 'numbers', 'letters', 'grammar']
    },
    
    'physical': {
        'description': 'Physical humor involves descriptions of bodily mishaps, clumsiness, slapstick scenarios, or minor injuries. The humor requires understanding of physical causation and embodied experience.',
        'instruction': 'about a physical mishap, collision, or clumsy action. The humor should come from the physical consequence itself.',
        'example_topics': ['walking into things', 'tripping', 'dropping objects', 'coordination failures']
    },
    
    'social': {
        'description': 'Social humor involves awkward situations, social norm violations, misunderstandings, or embarrassing moments in interpersonal contexts. Requires understanding of social expectations.',
        'instruction': 'about a socially awkward situation or social norm violation. The humor should emerge from social context and expectations.',
        'example_topics': ['awkward conversations', 'social mishaps', 'etiquette violations', 'miscommunications']
    },
    
    'dark': {
        'description': 'Dark humor addresses mortality, danger, taboo topics, or serious threats in a way that reframes them as non-threatening. Requires transformation of genuine threat into benign violation.',
        'instruction': 'about mortality, danger, or taboo topics, but in a way that makes the threat benign. Should be edgy but not offensive.',
        'example_topics': ['mortality', 'accidents', 'misfortune', 'existential dread']
    }
}

def generate_prompt(category: str, novel_context: str = None) -> str:
    """
    Generate category-specific prompt for joke generation.
    
    Args:
        category: One of ['linguistic', 'physical', 'social', 'dark']
        novel_context: Optional specific context to ensure novelty
        
    Returns:
        Complete prompt string
    """
    if category not in CATEGORY_SPECS:
        raise ValueError(f"Invalid category: {category}")
    
    spec = CATEGORY_SPECS[category]
    
    prompt = BASE_TEMPLATE.format(
        category=category,
        category_description=spec['description'],
        category_specific_instruction=spec['instruction']
    )
    
    # Add novel context if provided
    if novel_context:
        prompt += f"\n\nSpecific context for this joke: {novel_context}"
    
    return prompt

# Novel contexts to minimize training data retrieval
NOVEL_CONTEXTS = {
    'linguistic': [
        'a pun about quantum computing and breakfast',
        'wordplay involving origami and philosophy',
        'semantic ambiguity about semicolons and life choices',
        'double meaning with cryptocurrency and gardening',
        'homonym joke about asteroids and grammar'
    ],
    'physical': [
        'someone organizing a filing cabinet',
        'trying to fold a fitted sheet for the first time',
        'assembling furniture with unclear instructions',
        'using a standing desk incorrectly',
        'attempting to use chopsticks while wearing mittens'
    ],
    'social': [
        'accidentally joining a work video call in the wrong context',
        'misinterpreting a Slack emoji reaction',
        'LinkedIn networking gone wrong',
        'virtual background malfunction during serious meeting',
        'replying-all to an email chain'
    ],
    'dark': [
        'procrastination and deadline mortality',
        'existential dread at the DMV',
        'inbox zero as life goal',
        'retirement planning in your 20s',
        'reading the terms and conditions'
    ]
}

def get_novel_prompts(category: str, n: int = 5) -> list:
    """Generate n prompts with novel contexts for a category."""
    contexts = NOVEL_CONTEXTS[category][:n]
    return [generate_prompt(category, context) for context in contexts]

# Test function
if __name__ == '__main__':
    print("=== LINGUISTIC PROMPT ===")
    print(generate_prompt('linguistic', NOVEL_CONTEXTS['linguistic'][0]))
    print("\n=== PHYSICAL PROMPT ===")
    print(generate_prompt('physical', NOVEL_CONTEXTS['physical'][0]))