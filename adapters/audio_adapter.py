"""
Audio Adapter for Text-to-Speech and Speech-to-Text
"""

import os
from gtts import gTTS
import requests
import base64
from io import BytesIO
import tempfile

class AudioAdapter:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
    
    def text_to_speech(self, 
                      text: str, 
                      language: str = 'id',
                      slow: bool = False) -> Dict[str, Any]:
        """
        Convert text to speech using gTTS
        """
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                audio_path = tmp_file.name
            
            # Read the audio file as base64
            with open(audio_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Clean up temp file
            os.unlink(audio_path)
            
            return {
                'success': True,
                'audio_base64': audio_base64,
                'text': text,
                'language': language,
                'duration_estimate': len(text) / 15  # Rough estimate in seconds
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error generating speech: {str(e)}"
            }
    
    def speech_to_text(self, audio_file_path: str, language: str = 'id') -> Dict[str, Any]:
        """
        Convert speech to text using Hugging Face API
        """
        try:
            # Using Whisper model
            api_url = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
            
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            with open(audio_file_path, "rb") as f:
                audio_bytes = f.read()
            
            # Make API request
            response = requests.post(
                api_url, 
                headers=headers, 
                data=audio_bytes,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'text': result.get('text', ''),
                    'language': language,
                    'model': 'whisper-large-v3'
                }
            else:
                return {
                    'success': False,
                    'error': f"API Error: {response.status_code}",
                    'details': response.json()
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Error transcribing audio: {str(e)}"
            }
    
    def detect_language(self, text: str) -> str:
        """
        Simple language detection for TTS
        """
        # Check for Indonesian words
        indo_words = ['yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'dengan']
        english_words = ['the', 'and', 'in', 'to', 'from', 'for', 'with']
        
        indo_count = sum(1 for word in indo_words if word in text.lower())
        english_count = sum(1 for word in english_words if word in text.lower())
        
        return 'id' if indo_count > english_count else 'en'
