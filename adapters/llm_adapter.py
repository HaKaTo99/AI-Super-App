"""
LLM Adapter for Groq API
"""

import os
from groq import Groq
from typing import Optional, Dict, Any
import json

class LLMAdapter:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.client = Groq(api_key=self.api_key)
        
        # Available models on Groq
        self.models = {
            'fast': 'llama-3.2-3b-preview',        # Very fast, good for simple tasks
            'balanced': 'llama-3.2-11b-vision-preview', # Balanced speed & quality
            'quality': 'llama-3.1-70b-versatile',  # Best quality, slower
            'code': 'llama-3.2-11b-vision-preview',     # Good for code
            'vision': 'llama-3.2-11b-vision-preview'    # Image understanding
        }
    
    def generate_text(self, 
                     prompt: str, 
                     model_type: str = 'balanced',
                     system_prompt: str = None,
                     max_tokens: int = 1024,
                     temperature: float = 0.7,
                     context: str = None) -> Dict[str, Any]:
        """
        Generate text using Groq API
        """
        try:
            # Prepare messages
            messages = []
            
            # System prompt
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            else:
                # Default system prompt
                messages.append({
                    "role": "system",
                    "content": """You are a helpful AI assistant. Provide accurate, 
                    concise, and helpful responses. If you don't know something, 
                    say so honestly. Respond in the same language as the user."""
                })
            
            # Add context if provided
            if context:
                messages.append({
                    "role": "user",
                    "content": f"Context from previous conversation:\n{context}\n\nNow: {prompt}"
                })
            else:
                messages.append({
                    "role": "user",
                    "content": prompt
                })
            
            # Select model
            model = self.models.get(model_type, self.models['balanced'])
            
            # Make API call
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stream=False
            )
            
            # Parse response
            result = {
                'text': response.choices[0].message.content,
                'model': model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                },
                'success': True
            }
            
            return result
            
        except Exception as e:
            return {
                'text': f"Error generating text: {str(e)}",
                'model': 'error',
                'usage': {'total_tokens': 0},
                'success': False,
                'error': str(e)
            }
    
    def analyze_image(self, prompt: str, image_url: str = None, image_base64: str = None):
        """
        Analyze image using vision model
        Note: Groq's vision model requires specific format
        """
        try:
            messages = []
            
            if image_url or image_base64:
                # Vision model requires specific message format
                vision_message = {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ]
                }
                
                if image_url:
                    vision_message["content"].append({
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    })
                elif image_base64:
                    vision_message["content"].append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                    })
                
                messages.append(vision_message)
            
            response = self.client.chat.completions.create(
                model=self.models['vision'],
                messages=messages,
                max_tokens=1024
            )
            
            return {
                'text': response.choices[0].message.content,
                'success': True
            }
            
        except Exception as e:
            return {
                'text': f"Error analyzing image: {str(e)}",
                'success': False
            }
    
    def get_available_models(self) -> list:
        """Get list of available models"""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except:
            return list(self.models.values())
