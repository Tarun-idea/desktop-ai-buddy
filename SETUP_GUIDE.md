# 🚀 Desktop AI Buddy - Setup Guide

Complete step-by-step guide to get your AI buddy running!

## Prerequisites

- Python 3.8 or higher
- 4GB+ RAM recommended
- Internet connection (for initial setup and weather data)

## Step 1: Install Ollama

Ollama is the AI engine that powers your buddy.

### Windows & macOS:
1. Visit [ollama.ai](https://ollama.ai)
2. Click "Download"
3. Follow installation instructions
4. Open terminal/command prompt and run:
   ```bash
   ollama pull mistral
   ```

### Linux:
```bash
curl https://ollama.ai/install.sh | sh
ollama pull mistral
```

**Verify Ollama is running:**
```bash
ollama serve
```

You should see: `listening on 127.0.0.1:11434`

## Step 2: Clone the Repository

```bash
git clone https://github.com/Tarun-idea/desktop-ai-buddy.git
cd desktop-ai-buddy
```

## Step 3: Create Virtual Environment (Optional but Recommended)

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Run the Application

```bash
python src/main.py
```

You should see the Desktop AI Buddy window! 🎉

## Troubleshooting

### "Ollama is not running" Error
- Make sure Ollama server is started: `ollama serve`
- Run in a separate terminal/window

### "Model not found" Error
```bash
ollama pull mistral
```

### "Port 11434 already in use"
Change `OLLAMA_HOST` in `config.py` to a different port

### Slow responses
- Make sure you have enough RAM free
- Try a smaller model: `ollama pull neural-chat`

### Weather not updating
- Check your internet connection
- Verify location name in `config.py`

## Configuration

Edit `config.py` to customize:

```python
# AI Model
AI_MODEL = "mistral"  # Options: mistral, llama2, neural-chat

# Location for weather
LOCATION = "New York"

# Buddy name
BUDDY_NAME = "DESK-Buddy"
```

## Available Models

```bash
# Fast & lightweight (recommended for most users)
ollama pull neural-chat

# Balanced (good quality & speed)
ollama pull mistral

# High quality (slower)
ollama pull llama2

# Creative writing
ollama pull dolphin-mixtral
```

Switch models by editing `config.py`:
```python
AI_MODEL = "neural-chat"  # Change this
```

Then pull the model if you haven't:
```bash
ollama pull neural-chat
```

## Features Guide

### Chat with Your Buddy
- Type messages and press `Shift + Enter` to send
- Or click the Send button

### Emotions
- Buddy displays different emotions based on conversation
- 😊 Happy, 😢 Sad, 🤔 Thinking, 🤩 Excited, etc.

### Weather Display
- Shows real-time weather for your location
- Updates every 10 minutes automatically

### Time Display
- Shows current time in top-right corner

## Tips for Best Experience

1. **Keep Ollama running** - Start it before launching the app
2. **Choose right model** - Smaller models = faster responses
3. **Update location** - Edit `config.py` for accurate weather
4. **Keep chat focused** - Keep messages clear and concise
5. **Clear history** - App remembers last 20 messages for context

## Next Steps

- Customize the appearance in `config.py`
- Try different AI models
- Add your location for weather
- Explore voice features (coming soon!)

## System Requirements

### Minimum:
- 4GB RAM
- 2GB storage (for model)
- CPU: Intel i5 or equivalent
- OS: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### Recommended:
- 8GB+ RAM
- 10GB+ storage
- GPU (NVIDIA, AMD, or Apple Silicon) for faster responses
- Ollama supports GPU acceleration!

## Getting Help

- Check [Ollama documentation](https://ollama.ai)
- Open a GitHub issue
- Check the troubleshooting section above

## What's Next?

- ✨ Voice input/output (future)
- 🎨 More customization options
- 🔌 Plugin system
- 🌍 Multi-language support

---

**Happy chatting with your AI buddy!** 🤖
