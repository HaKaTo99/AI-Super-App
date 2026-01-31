"""
Utility functions for AI adapters
"""

import re
import json
from typing import Dict, Any
import base64
from io import BytesIO
from PIL import Image

def sanitize_prompt(prompt: str) -> str:
    """
    Sanitize user prompt for safe API calls
    """
    # Remove excessive whitespace
    prompt = re.sub(r'\s+', ' ', prompt).strip()
    
    # Limit length
    if len(prompt) > 1000:
        prompt = prompt[:1000] + "..."
    
    return prompt

def format_response(response_type: str, data: Dict[str, Any]) -> str:
    """
    Format response based on type
    """
    if response_type == 'text':
        return data.get('text', '')
    
    elif response_type == 'image':
        return f"![Generated Image](data:image/png;base64,{data.get('image_base64', '')})"
    
    elif response_type == 'audio':
        return f"🔊 Audio generated ({data.get('duration_estimate', 0):.1f}s)"
    
    elif response_type == 'error':
        return f"❌ Error: {data.get('error', 'Unknown error')}"
    
    return str(data)

def image_to_base64(image: Image.Image) -> str:
    """
    Convert PIL Image to base64 string
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def base64_to_image(base64_str: str) -> Image.Image:
    """
    Convert base64 string to PIL Image
    """
    image_data = base64.b64decode(base64_str)
    return Image.open(BytesIO(image_data))

def estimate_token_count(text: str) -> int:
    """
    Rough estimate of token count
    """
    # Approximate: 1 token ≈ 4 characters for English
    return len(text) // 4

def get_model_info(model_type: str) -> Dict[str, str]:
    """
    Get information about different model types
    """
    model_info = {
        'llm': {
            'name': 'Llama 3.2 (Groq)',
            'capabilities': 'Text generation, reasoning, coding',
            'limit': '~30 requests/minute (free tier)'
        },
        'image': {
            'name': 'Stable Diffusion (Hugging Face)',
            'capabilities': 'Image generation from text',
            'limit': '~1000 inferences/month (free tier)'
        },
        'audio': {
            'name': 'gTTS & Whisper',
            'capabilities': 'Text-to-speech and speech-to-text',
            'limit': 'Unlimited (gTTS), ~1000/month (Whisper)'
        }
    }
    
    return model_info.get(model_type, {})
