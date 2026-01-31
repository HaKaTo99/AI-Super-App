# 🚀 Deployment Guide - AI Super App

## Option 1: Streamlit Cloud (Recommended)

### Prerequisites
1. GitHub account
2. Streamlit account (free)
3. API keys from Groq and Hugging Face

### Steps
1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/ai-super-app.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository and branch
   - Set main file to `app.py`
   - Add secrets in Advanced Settings:
     ```
     GROQ_API_KEY=your_actual_key_here
     HUGGINGFACE_API_KEY=your_actual_key_here
     ```

3. **Access your app**
   - Your app will be available at: `https://your-app-name.streamlit.app`

## Option 2: Hugging Face Spaces

### Steps
1. Create new Space on Hugging Face
2. Select "Streamlit" as SDK
3. Upload all files
4. Add secrets in Settings → Repository secrets
5. Your app will be at: `https://huggingface.co/spaces/yourusername/ai-super-app`

## Option 3: Local Deployment

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/ai-super-app.git
cd ai-super-app

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Run the app
streamlit run app.py
```

## Environment Variables
Create a `.env` file with:
```env
GROQ_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Getting API Keys

### Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up/login
3. Navigate to API Keys
4. Click "Create API Key"
5. Copy the key

### Hugging Face API Key
1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Sign up/login
3. Click "New token"
4. Select "Read" access
5. Copy the token

## Troubleshooting

### Common Issues

1. **API Rate Limits**
   - Groq: ~30 requests/minute on free tier
   - Hugging Face: ~1000 inferences/month
   - Solution: Implement caching and use fallback models

2. **Model Loading Time**
   - First request might be slow
   - Solution: Use smaller models or implement loading indicators

3. **Memory Issues**
   - Clear chat history regularly
   - Restart the app if it becomes slow

4. **API Key Errors**
   - Verify keys are correctly set
   - Check if keys have expired
   - Regenerate keys if needed

## Scaling Tips

1. **Implement Caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_llm_call(prompt):
       return llm_adapter.generate_text(prompt)
   ```

2. **Use Async Calls**
   ```python
   import asyncio
   
   async def process_multiple_requests(requests):
       tasks = [process_request(req) for req in requests]
       return await asyncio.gather(*tasks)
   ```

3. **Monitor Usage**
   - Track API calls per user
   - Implement rate limiting
   - Set usage quotas

## Security Considerations

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Implement user authentication** for production
4. **Add rate limiting** to prevent abuse
5. **Log API usage** for monitoring

## Cost Management

### Free Tier Limits
- Groq: Unlimited on free tier (with rate limits)
- Hugging Face: ~$10 free credits/month
- Total estimated cost for MVP: $0/month

### If You Scale
- Consider premium tiers
- Implement user accounts with quotas
- Add subscription model
- Use cheaper models for simple tasks
