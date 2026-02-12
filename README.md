# AI Super App

Aplikasi yang menggabungkan semua AI gratis dalam satu antarmuka.

## Fitur
- Chat dengan AI (Groq Llama 3.2)
- Generate gambar (Stable Diffusion)
- Text-to-speech (gTTS)
- Speech-to-text (Whisper)
- Upload & analisis file

## Instalasi Cepat

```bash
# 1. Clone atau buat folder
mkdir ai-super-app
cd ai-super-app

# 2. Buat file requirements.txt dan app.py
# (Salin kode dari dokumentasi ini)

# 3. Install dependencies
pip install streamlit python-dotenv requests pillow gtts

# 4. Buat file .env
echo "GROQ_API_KEY=your_key_here" > .env
echo "HUGGINGFACE_API_KEY=your_key_here" >> .env

# 5. Jalankan aplikasi
streamlit run app.py
```

## Dapatkan API Key Gratis

1. **Groq API**: https://console.groq.com
2. **Hugging Face**: https://huggingface.co/settings/tokens

## Cara Menggunakan

1. **Chat**: Ketik pesan seperti biasa
2. **Gambar**: Ketik "buat gambar [deskripsi]"
3. **Audio**: Ketik "baca teks ini" untuk TTS
4. **Upload**: Upload gambar/audio untuk analisis

##  Deployment

### Streamlit Cloud (Gratis)
1. Push ke GitHub
2. Buka https://share.streamlit.io
3. Deploy dengan secrets untuk API keys

## Bantuan

Jika ada masalah:
1. Cek API keys di sidebar
2. Pastikan internet tersambung
3. Coba reload aplikasi

---

**Dibuat dengan ❤️ untuk komunitas AI Indonesia**
