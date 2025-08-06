# 🤖 Ollama Chat Studio

Welcome to **Ollama Chat Studio** – your sleek, powerful, and fun-to-use interface for chatting with local AI models! 🚀

Built with ❤️ by Brian Laughlin, this Streamlit-powered application transforms your conversations with AI into an engaging, customizable experience.

## ✨ Features

- 🎨 **Dark & Light Themes** - Switch between themes with a single click
- 🤝 **Model Comparison** - Chat with multiple models side-by-side
- 🧠 **Thinking Process Visualization** - See how models like DeepSeek-R1 think
- ⚙️ **Advanced Parameters** - Fine-tune temperature, top-p, and max tokens
- 💾 **Export Conversations** - Save your chats in JSON, Markdown, or plain text
- 📊 **Real-time Statistics** - Monitor token usage and generation speed
- 🎯 **System Prompts** - Customize model behavior with custom instructions
- 🔄 **Regenerate Responses** - Don't like an answer? Try again!

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running (see installation guide below)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <your-repo-url>
   cd ollama-chat
   ```

2. **Install Python dependencies**
   ```bash
   pip install streamlit requests
   ```
   
   Or if you prefer using a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install streamlit requests
   ```

3. **Run the application**
   ```bash
   streamlit run ollama-chat-app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

That's it! You're ready to chat! 🎉

## 🦙 Installing Ollama

Ollama is the magic behind running local AI models. Here's how to get it set up:

### 🪟 Windows Installation

1. **Download Ollama**
   - Visit [ollama.ai](https://ollama.ai)
   - Click "Download for Windows"
   - Run the installer (.exe file)

2. **Verify Installation**
   - Open Command Prompt or PowerShell
   - Type: `ollama --version`
   - You should see version information

3. **Start Ollama Service**
   - Ollama usually starts automatically
   - If not, run: `ollama serve`

### 🍎 macOS Installation

**Option 1: Direct Download**
1. Visit [ollama.ai](https://ollama.ai)
2. Click "Download for Mac"
3. Open the downloaded .dmg file
4. Drag Ollama to your Applications folder

**Option 2: Homebrew** (if you're a brew user)
```bash
brew install ollama
```

**Start Ollama:**
```bash
ollama serve
```

### 🐧 Linux Installation

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

Then start the service:
```bash
ollama serve
```

## 🧠 Downloading AI Models

Once Ollama is installed, you can download models with a simple command:

### Popular Models to Try:

**🚀 Fast & Efficient:**
```bash
ollama pull llama3.2:3b          # Great for quick responses
ollama pull phi3:mini            # Microsoft's compact model
```

**🎯 Balanced Performance:**
```bash
ollama pull llama3.2:8b          # Good balance of speed and quality
ollama pull mistral:7b           # Excellent instruction following
```

**🧠 High Performance:**
```bash
ollama pull llama3.2:70b         # Top-tier responses (requires more RAM)
ollama pull codellama:13b        # Excellent for coding tasks
```

**🤔 Reasoning Models:**
```bash
ollama pull deepseek-r1:7b       # Shows thinking process
ollama pull qwen2.5:14b          # Great reasoning capabilities
```

### Model Requirements:
- **3B models**: ~2GB RAM
- **7B models**: ~4GB RAM
- **13B models**: ~8GB RAM
- **70B models**: ~40GB RAM

💡 **Pro Tip**: Start with `llama3.2:3b` or `phi3:mini` if you're new to local AI!

## 🎮 How to Use

1. **Start the App**: Run `streamlit run ollama-chat-app.py`
2. **Select a Model**: Choose from your downloaded models in the sidebar
3. **Customize Settings**: Adjust temperature, system prompts, and more
4. **Start Chatting**: Type your message and hit Enter!

### 🎨 Cool Features to Try:

- **🌙 Theme Toggle**: Switch between dark and light modes
- **🤝 Model Comparison**: Enable "Compare Models" to chat with multiple AIs simultaneously
- **🤔 Thinking Process**: With models like DeepSeek-R1, expand the "Thinking Process" to see the AI's reasoning
- **💾 Export Chats**: Save your conversations for later review
- **🔄 Regenerate**: Don't like a response? Click regenerate for a different answer!

## 🛠️ Advanced Configuration

### System Prompts
Customize how the AI behaves by setting system prompts like:
- "You are a helpful coding assistant"
- "Respond only in haikus"
- "You are a friendly teacher explaining complex topics simply"

### Parameter Tuning
- **Temperature** (0.0-2.0): Controls creativity (lower = more focused)
- **Top P** (0.0-1.0): Controls response diversity
- **Max Tokens**: Limits response length

## 🐛 Troubleshooting

**Ollama not connecting?**
- Make sure Ollama is running: `ollama serve`
- Check if it's accessible: `curl http://localhost:11434/api/tags`

**No models showing?**
- Download a model first: `ollama pull llama3.2:3b`
- Restart the Streamlit app

**App running slowly?**
- Try smaller models (3B or 7B parameters)
- Reduce max tokens
- Close other memory-intensive applications

## 📝 License & Rights

This project is licensed under the **MIT License** - see below for details:

```
MIT License

Copyright (c) 2024 Brian Laughlin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🤝 Contributing

Found a bug? Have a cool feature idea? Contributions are welcome! Feel free to:
- Open an issue
- Submit a pull request
- Share your feedback

## 🎉 Acknowledgments

- **Ollama Team** - For making local AI accessible
- **Streamlit** - For the amazing web app framework
- **The Open Source Community** - For making projects like this possible

---

**Happy Chatting!** 🚀✨

*Made with ❤️ and lots of ☕ by Brian Laughlin*