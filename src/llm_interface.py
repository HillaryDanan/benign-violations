"""
Unified interface for calling different LLM providers.
Handles API differences and provides consistent error handling.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
from typing import Dict, Any
import openai
import anthropic
import google.generativeai as genai
from src.config import (
    OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, MODELS
)

# Initialize clients
openai.api_key = OPENAI_API_KEY
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)

class LLMInterface:
    """Unified interface for multiple LLM providers."""
    
    def __init__(self, model_key: str):
        """
        Initialize LLM interface.
        
        Args:
            model_key: One of ['gpt4o', 'claude', 'gemini']
        """
        if model_key not in MODELS:
            raise ValueError(f"Invalid model: {model_key}")
        
        self.model_key = model_key
        self.config = MODELS[model_key]
        self.provider = self.config['provider']
        self.model_name = self.config['name']
        
    def generate(self, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate completion from LLM.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            
        Returns:
            Dictionary with 'text', 'model', 'tokens', 'latency'
        """
        start_time = time.time()
        
        try:
            if self.provider == 'openai':
                response = self._call_openai(prompt, temperature)
            elif self.provider == 'anthropic':
                response = self._call_anthropic(prompt, temperature)
            elif self.provider == 'google':
                response = self._call_google(prompt, temperature)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            
            latency = time.time() - start_time
            response['latency'] = latency
            response['model'] = self.model_name
            response['temperature'] = temperature
            
            return response
            
        except Exception as e:
            return {
                'text': None,
                'error': str(e),
                'model': self.model_name,
                'temperature': temperature,
                'latency': time.time() - start_time
            }
    
    def _call_openai(self, prompt: str, temperature: float) -> Dict:
        """Call OpenAI API."""
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=self.config['max_tokens']
        )
        
        return {
            'text': response.choices[0].message.content,
            'tokens': response.usage.total_tokens,
            'finish_reason': response.choices[0].finish_reason
        }
    
    def _call_anthropic(self, prompt: str, temperature: float) -> Dict:
        """Call Anthropic API."""
        response = anthropic_client.messages.create(
            model=self.model_name,
            max_tokens=self.config['max_tokens'],
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            'text': response.content[0].text,
            'tokens': response.usage.input_tokens + response.usage.output_tokens,
            'finish_reason': response.stop_reason
        }
    
    def _call_google(self, prompt: str, temperature: float) -> Dict:
        """Call Google Gemini API."""
        model = genai.GenerativeModel(self.model_name)
        
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=self.config['max_tokens']
        )
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return {
            'text': response.text,
            'tokens': None,  # Gemini doesn't always return token counts
            'finish_reason': 'complete'
        }

# Test function
if __name__ == '__main__':
    # Quick test
    llm = LLMInterface('gpt4o')
    result = llm.generate("Tell me a short pun about computers.", temperature=0.7)
    print(f"Response: {result['text']}")
    print(f"Latency: {result['latency']:.2f}s")