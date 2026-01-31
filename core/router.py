"""
Smart Router for AI Super App
Detects user intent and routes to appropriate AI model
"""

import re
from langdetect import detect

class IntentRouter:
    def __init__(self):
        self.keyword_patterns = {
            'image_generation': [
                r'gambar', r'foto', r'image', r'generate.*image',
                r'buat.*gambar', r'buat.*foto', r'buat.*visual',
                r'illustrasi', r'lukis', r'gambar.*kan',
                r'create.*image', r'draw', r'painting'
            ],
            'image_analysis': [
                r'analisis.*gambar', r'jelaskan.*gambar',
                r'apa.*ini.*gambar', r'deskripsi.*gambar',
                r'identifikasi.*gambar', r'what.*image',
                r'describe.*image', r'analyze.*image'
            ],
            'audio_generation': [
                r'suara', r'audio', r'bacakan', r'baca.*keras',
                r'convert.*teks.*suara', r'text.*to.*speech',
                r'tts', r'dengarkan', r'speak',
                r'ubah.*teks.*suara', r'narasikan'
            ],
            'transcription': [
                r'transkrip', r'transcribe', r'suara.*ke.*teks',
                r'audio.*ke.*teks', r'speech.*to.*text',
                r'stt', r'ubah.*suara.*teks'
            ],
            'code_generation': [
                r'kode', r'program', r'function', r'script',
                r'buat.*kode', r'write.*code', r'programming',
                r'coding', r'fungsi', r'algorithm'
            ],
            'translation': [
                r'translate', r'terjemah', r'bahasa',
                r'inggris.*indonesia', r'indonesia.*inggris',
                r'english.*indonesian', r'indonesian.*english'
            ],
            'summary': [
                r'ringkas', r'summary', r'summarize',
                r'intisari', r'kesimpulan', r'poin.*penting'
            ]
        }
        
        # Image extensions
        self.image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
    
    def detect_intent(self, user_input, uploaded_file=None):
        """
        Detect user intent from input and uploaded files
        Returns: (intent_type, confidence, parameters)
        """
        input_lower = user_input.lower()
        
        # Check if user uploaded a file
        if uploaded_file:
            file_extension = uploaded_file.name.lower()
            
            # Check if it's an image file
            if any(ext in file_extension for ext in self.image_extensions):
                return 'image_analysis', 0.9, {'file_type': 'image'}
            
            # Check if it's an audio file
            elif any(ext in file_extension for ext in ['.mp3', '.wav', '.m4a', '.ogg']):
                return 'transcription', 0.9, {'file_type': 'audio'}
        
        # Detect language
        try:
            lang = detect(user_input)
        except:
            lang = 'en'
        
        # Check for keyword patterns
        intent_scores = {}
        
        for intent, patterns in self.keyword_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, input_lower):
                    score += 1
            
            if score > 0:
                intent_scores[intent] = score
        
        # Default to text generation
        if not intent_scores:
            return 'text_generation', 0.8, {'language': lang}
        
        # Get intent with highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[best_intent] / 3, 1.0)  # Normalize to 0-1
        
        # Additional parameters
        params = {
            'language': lang,
            'has_question': '?' in user_input,
            'length': len(user_input.split()),
            'requires_creative': any(word in input_lower for word in ['kreatif', 'creative', 'imajinasi', 'imagination'])
        }
        
        return best_intent, confidence, params
    
    def route_request(self, intent, user_input, params=None):
        """
        Route the request to appropriate handler
        """
        routing_map = {
            'text_generation': 'llm',
            'image_generation': 'image',
            'image_analysis': 'llm',  # Use LLM with vision capability
            'audio_generation': 'audio',
            'transcription': 'audio',
            'code_generation': 'llm',
            'translation': 'llm',
            'summary': 'llm'
        }
        
        return routing_map.get(intent, 'llm')
