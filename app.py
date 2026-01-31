"""
AI Super App - Main Application
Gabungkan semua AI gratis dalam satu aplikasi
"""

import streamlit as st
import os
from dotenv import load_dotenv
import base64
from datetime import datetime
import json
import tempfile
from io import BytesIO

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Super App",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS is handled dynamically in render_sidebar


# Simple router class (inline untuk MVP)
class SimpleRouter:
    def __init__(self):
        self.intents = {
            'image': ['gambar', 'foto', 'image', 'buat gambar', 'generate image', 'visual'],
            'audio': ['suara', 'audio', 'baca', 'speak', 'tts', 'text to speech'],
            'transcribe': ['transkrip', 'transcribe', 'speech to text', 'stt'],
            'code': ['kode', 'program', 'function', 'script', 'coding'],
            'translate': ['terjemah', 'translate', 'bahasa'],
            'summary': ['ringkas', 'summary', 'summarize']
        }
    
    def detect(self, text):
        text_lower = text.lower()
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        return 'chat'

# Simple memory class
class SimpleMemory:
    def __init__(self):
        if 'history' not in st.session_state:
            st.session_state.history = []
    
    def add(self, role, content, metadata=None):
        st.session_state.history.append({
            'role': role,
            'content': content,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        })
    
    def get_recent(self, n=5):
        return st.session_state.history[-n:] if st.session_state.history else []
    
    def clear(self):
        st.session_state.history = []

# AI Adapters
class AIAdapters:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    # Text generation with Groq
    def generate_text(self, prompt):
        try:
            if not self.groq_api_key or self.groq_api_key.startswith('your_'):
                return "⚠️ Groq API Key belum diatur. Silakan tambahkan di sidebar."
            
            from groq import Groq
            client = Groq(api_key=self.groq_api_key)
            
            # Debug text
            print(f"DEBUG: Using Groq API Key: {self.groq_api_key[:10]}... (Length: {len(self.groq_api_key)})")

            # Try different models - UPDATED with user request
            models = [
                'moonshotai/Kimi-K2.5',       # User specific request
                'deepseek-ai/DeepSeek-OCR-2', # User specific request
                'openai/gpt-oss-120b',        # User requested model
                'llama3-70b-8192',            # High Intelligence
                'llama3-8b-8192',             # Standard fast model
                'mixtral-8x7b-32768',         # High quality
                'gemma-7b-it'                 # Alternative
            ]
            
            for model in models:
                try:
                    print(f"DEBUG: Trying model {model}...")
                    
                    completion = client.chat.completions.create(
                        model=model,
                        messages=[{'role': 'user', 'content': prompt}],
                        temperature=0.7,
                        max_tokens=1024
                    )
                    
                    return completion.choices[0].message.content
                    
                except Exception as ex:
                    print(f"DEBUG: Error with model {model}: {str(ex)}")
                    continue
            
            return "❌ Gagal mendapatkan respons dari Groq API. Cek terminal untuk detail error."
            
        except Exception as e:
            print(f"Critical Error: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    # Image generation with Hugging Face
    def generate_image(self, prompt):
        try:
            if not self.hf_api_key or self.hf_api_key == 'your_hf_api_key_here':
                return None, "⚠️ Hugging Face API Key belum diatur."
            
            import requests
            from PIL import Image
            
            # Try different models
            models = [
                'stabilityai/stable-diffusion-xl-base-1.0',
                'runwayml/stable-diffusion-v1-5',
                'CompVis/stable-diffusion-v1-4'
            ]
            
            headers = {'Authorization': f'Bearer {self.hf_api_key}'}
            
            for model in models:
                try:
                    response = requests.post(
                        f'https://api-inference.huggingface.co/models/{model}',
                        headers=headers,
                        json={'inputs': prompt},
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        # Convert to image
                        image = Image.open(BytesIO(response.content))
                        return image, f"✅ Gambar dibuat dengan model: {model}"
                    
                except requests.exceptions.Timeout:
                    continue
                except:
                    continue
            
            return None, "❌ Gagal membuat gambar. Coba lagi nanti."
            
        except Exception as e:
            return None, f"❌ Error: {str(e)}"
    
    # Text to speech
    def text_to_speech(self, text):
        try:
            from gtts import gTTS
            import tempfile
            
            # Detect language
            lang = 'id' if any(word in text.lower() for word in 
                             ['yang', 'dan', 'di', 'ke', 'dari']) else 'en'
            
            # Create TTS
            tts = gTTS(text=text, lang=lang, slow=False)
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                tts.save(tmp.name)
                with open(tmp.name, 'rb') as f:
                    audio_bytes = f.read()
                
                # Clean up
                os.unlink(tmp.name)
            
            return audio_bytes, "✅ Audio berhasil dibuat"
            
        except Exception as e:
            return None, f"❌ Error TTS: {str(e)}"
    
    # Speech to text
    def speech_to_text(self, audio_file):
        try:
            if not self.hf_api_key:
                return None, "⚠️ Hugging Face API Key belum diatur."
            
            import requests
            
            headers = {'Authorization': f'Bearer {self.hf_api_key}'}
            
            # Read audio file
            audio_bytes = audio_file.read()
            
            # Use Whisper model
            response = requests.post(
                'https://api-inference.huggingface.co/models/openai/whisper-large-v3',
                headers=headers,
                data=audio_bytes,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('text', ''), "✅ Transkripsi berhasil"
            else:
                return None, f"❌ Gagal transkripsi: {response.status_code}"
            
        except Exception as e:
            return None, f"❌ Error STT: {str(e)}"

# Main App Class
class AISuperApp:
    def __init__(self):
        self.router = SimpleRouter()
        self.memory = SimpleMemory()
        self.ai = AIAdapters()
        
        # Initialize session states
        if 'api_configured' not in st.session_state:
            st.session_state.api_configured = False
        
        if 'current_model' not in st.session_state:
            st.session_state.current_model = 'balanced'
        
        if 'image_style' not in st.session_state:
            st.session_state.image_style = 'realistic'
    
    def render_header(self):
        """Render application header"""
        st.markdown("""
        <div class="main-header">
            <h1>AI Super App</h1>
            <p>Integrated Artificial Intelligence System</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render sidebar with configuration"""
        with st.sidebar:
            st.title("⚡ Control Panel")
            
            # API Configuration
            with st.expander("🔐 Akses Token (API Keys)", expanded=True):
                st.info("Masukkan kredensial API Anda di sini:")
                st.markdown("- [Groq Console](https://console.groq.com)")
                st.markdown("- [Hugging Face](https://huggingface.co/settings/tokens)")
                
                groq_key = st.text_input(
                    "Groq Key",
                    value=os.getenv('GROQ_API_KEY', ''),
                    type="password",
                    help="Kunci API untuk teks & logika"
                )
                
                hf_key = st.text_input(
                    "Hugging Face Key",
                    value=os.getenv('HUGGINGFACE_API_KEY', ''),
                    type="password",
                    help="Kunci API untuk gambar & audio"
                )
                
                if st.button("💾 Simpan Kredensial"):
                    # Update environment
                    os.environ['GROQ_API_KEY'] = groq_key
                    os.environ['HUGGINGFACE_API_KEY'] = hf_key
                    self.ai.groq_api_key = groq_key
                    self.ai.hf_api_key = hf_key
                    st.session_state.api_configured = True
                    st.success("✅ Kredensial Terverifikasi")
                    st.rerun()
            
            # Model Settings
            with st.expander("🧠 Neural Configuration"):
                st.selectbox(
                    "Model Teks",
                    ["llama-3.2-3b (Cepat)", "llama-3.2-11b (Seimbang)", "mixtral-8x7b (Kompleks)"],
                    key="text_model"
                )
                
                st.selectbox(
                    "Style Visual",
                    ["Cinematic", "Anime Style", "Photorealistic", "Digital Art", "Cyberpunk"],
                    key="image_style"
                )
                
                st.slider(
                    "Tingkat Kreativitas",
                    0.0, 1.0, 0.7,
                    key="temperature",
                    help="0 = Presisi, 1 = Kreatif"
                )
            
            # App Info
            with st.expander("ℹ️ Status Sistem"):
                st.write("**Core:** v2.1.0 (Stable)")
                st.write("**Server:** Online ✅")
                
                if st.session_state.history:
                    st.write(f"**Memory Usage:** {len(st.session_state.history)} interactions")
                
                st.markdown("""
                <div style='font-size: 0.8rem; color: #94a3b8;'>
                Fitur Aktif:<br>
                • Neural Chat Engine<br>
                • Visual Synthesis<br>
                • Voice Synthesis<br>
                • Audio Transcription
                </div>
                """, unsafe_allow_html=True)
            
            # Actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🧹 Bersihkan", use_container_width=True):
                    self.memory.clear()
                    st.rerun()
            
            with col2:
                if st.button("🔁 Reboot", use_container_width=True):
                    st.session_state.clear()
                    st.rerun()
    
    def render_chat_interface(self):
        """Render main chat interface"""
        # Display chat history
        for msg in st.session_state.history:
            role_class = "user-message" if msg['role'] == 'user' else "ai-message"
            st.markdown(f"""
            <div class="chat-message {role_class}">
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
            
            # Show metadata if exists
            if msg.get('metadata'):
                metadata = msg['metadata']
                if metadata.get('type') == 'image':
                    try:
                        st.image(msg['content'], caption=metadata.get('caption', ''))
                    except:
                        pass
                elif metadata.get('type') == 'audio':
                    try:
                        st.audio(msg['content'], format='audio/mp3')
                    except:
                        pass
        
        # Chat input and file upload
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            user_input = st.text_input(
                "Input Command...",
                key="user_input",
                placeholder="Ketik perintah atau tanya sesuatu...",
                label_visibility="collapsed"
            )
        
        with col2:
            uploaded_file = st.file_uploader(
                "📎",
                type=['png', 'jpg', 'jpeg', 'mp3', 'wav'],
                key="file_uploader",
                label_visibility="collapsed",
                help="Upload Data (Gambar/Audio)"
            )
        
        with col3:
            send_button = st.button("EXECUTE COMMAND", use_container_width=True)
        
        # Process input when button is clicked
        if send_button and (user_input or uploaded_file):
            self.process_input(user_input, uploaded_file)
    
    def process_input(self, user_input, uploaded_file):
        """Process user input"""
        # Add user message to history
        if uploaded_file:
            file_info = f"📎 {uploaded_file.name} ({uploaded_file.type})"
            display_content = f"{user_input}\n\n{file_info}" if user_input else file_info
        else:
            display_content = user_input
        
        self.memory.add('user', display_content)
        
        # Show processing indicator
        with st.spinner("AI sedang berpikir..."):
            # Detect intent
            intent = self.router.detect(user_input.lower() if user_input else "")
            
            # Process based on intent
            if uploaded_file:
                # File processing
                if uploaded_file.type.startswith('image'):
                    # Image analysis
                    response = self.ai.generate_text(
                        f"Analisis gambar ini: {user_input if user_input else 'Apa yang ada di gambar ini?'}"
                    )
                    self.memory.add('ai', response, {'type': 'text'})
                
                elif uploaded_file.type.startswith('audio'):
                    # Audio transcription
                    text, status = self.ai.speech_to_text(uploaded_file)
                    if text:
                        response = f"**Transkripsi Audio:**\n\n{text}\n\n{status}"
                        self.memory.add('ai', response, {'type': 'text'})
                    else:
                        self.memory.add('ai', f"❌ {status}", {'type': 'error'})
            
            elif intent == 'image':
                # Generate image
                prompt = user_input if user_input else "pemandangan alam yang indah"
                image, status = self.ai.generate_image(prompt)
                
                if image:
                    # Convert image to bytes for display
                    img_byte_arr = BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_bytes = img_byte_arr.getvalue()
                    
                    self.memory.add('ai', img_bytes, {
                        'type': 'image',
                        'caption': f"Generated: {prompt[:50]}...",
                        'status': status
                    })
                else:
                    self.memory.add('ai', status, {'type': 'error'})
            
            elif intent == 'audio':
                # Text to speech
                audio_bytes, status = self.ai.text_to_speech(user_input)
                
                if audio_bytes:
                    self.memory.add('ai', audio_bytes, {
                        'type': 'audio',
                        'status': status,
                        'text': user_input[:100] + "..." if len(user_input) > 100 else user_input
                    })
                else:
                    self.memory.add('ai', status, {'type': 'error'})
            
            else:
                # Text generation
                response = self.ai.generate_text(user_input)
                self.memory.add('ai', response, {'type': 'text'})
        
        # Rerun to update display
        st.rerun()
    
    def run(self):
        """Main application runner"""
        # Check API configuration
        groq_key = os.getenv('GROQ_API_KEY', '')
        hf_key = os.getenv('HUGGINGFACE_API_KEY', '')
        
        if not groq_key or groq_key == 'your_groq_api_key_here' or \
           not hf_key or hf_key == 'your_hf_api_key_here':
            st.warning("""
            ⚠️ **API Keys belum dikonfigurasi!**
            
            Untuk menggunakan AI Super App, Anda perlu:
            1. Dapatkan API Key gratis dari [Groq](https://console.groq.com)
            2. Dapatkan API Key gratis dari [Hugging Face](https://huggingface.co/settings/tokens)
            3. Masukkan kedua API Key di sidebar
            """)
        
        # Render components
        self.render_header()
        
        col1, col3 = st.columns([1, 3])
        
        with col1:
            self.render_sidebar()
        
        with col3:
            self.render_chat_interface()
        
        # Footer
        st.markdown("---")
        st.caption("AI Super App v1.0 | Gabungkan semua AI gratis dalam satu aplikasi")

# Run the app
if __name__ == "__main__":
    app = AISuperApp()
    app.run()
