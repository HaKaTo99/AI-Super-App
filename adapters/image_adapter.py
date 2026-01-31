"""
Image Generation Adapter using Hugging Face API
"""

import os
import requests
import base64
from io import BytesIO
from PIL import Image
import json

class ImageAdapter:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        self.api_url = "https://api-inference.huggingface.co/models/"
        
        # Pre-defined models for different styles
        self.models = {
            'realistic': 'stabilityai/stable-diffusion-xl-base-1.0',
            'anime': 'digiplay/AbsoluteReality_v1.8.1',
            'cartoon': 'wavymulder/Analog-Diffusion',
            'art': 'prompthero/openjourney',
            'fast': 'CompVis/stable-diffusion-v1-4'
        }
    
    def generate_image(self, 
                      prompt: str, 
                      model_type: str = 'realistic',
                      negative_prompt: str = None,
                      num_inference_steps: int = 30,
                      guidance_scale: float = 7.5,
                      width: int = 512,
                      height: int = 512) -> Dict[str, Any]:
        """
        Generate image using Hugging Face API
        """
        try:
            # Select model
            model = self.models.get(model_type, self.models['realistic'])
            api_url = f"{self.api_url}{model}"
            
            # Prepare payload
            payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": num_inference_steps,
                    "guidance_scale": guidance_scale,
                    "width": width,
                    "height": height
                }
            }
            
            if negative_prompt:
                payload["parameters"]["negative_prompt"] = negative_prompt
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                api_url, 
                headers=headers, 
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                # Get image from response
                image_bytes = response.content
                
                # Convert to PIL Image
                image = Image.open(BytesIO(image_bytes))
                
                # Convert to base64 for HTML display
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                return {
                    'success': True,
                    'image': image,
                    'image_base64': img_str,
                    'model': model,
                    'prompt': prompt,
                    'dimensions': f"{width}x{height}"
                }
            else:
                error_msg = response.json().get('error', 'Unknown error')
                return {
                    'success': False,
                    'error': f"API Error: {error_msg}",
                    'status_code': response.status_code
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': "Request timed out. Model might be loading. Try again in a minute."
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error generating image: {str(e)}"
            }
    
    def get_available_models(self) -> list:
        """Get list of available models"""
        return list(self.models.keys())
    
    def analyze_image(self, image_path: str, prompt: str = "Describe this image in detail") -> Dict[str, Any]:
        """
        Analyze image using vision model
        """
        try:
            # Using a vision model
            model = "Salesforce/blip-image-captioning-large"
            api_url = f"{self.api_url}{model}"
            
            # Read and encode image
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            response = requests.post(
                api_url, 
                headers=headers, 
                data=image_bytes,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'description': result[0]['generated_text'],
                    'model': model
                }
            else:
                return {
                    'success': False,
                    'error': f"API Error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Error analyzing image: {str(e)}"
            }
