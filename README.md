# 💬 Local LLM Chat Application

A beautiful, ChatGPT-inspired chat interface for interacting with local Large Language Models (LLMs) using Ollama. All processing happens locally on your machine - completely private and secure with no data sent to external servers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- **🎨 Modern UI/UX**: Clean, ChatGPT-inspired interface with minimalist design
- **💬 Chat History**: Persistent chat storage with easy access to previous conversations
- **🤖 Multiple Models**: Support for various Ollama models (Llama3, Mistral, CodeLlama, etc.)
- **🔒 100% Private**: All processing happens locally - your data never leaves your machine
- **⚡ Real-time Responses**: Fast, streaming responses from local LLMs
- **📱 Responsive Design**: Works seamlessly on different screen sizes
- **🗂️ Session Management**: Create new chats, switch between conversations, and manage history

## 🏗️ Tech Stack

### **Frontend: Streamlit**
- **What**: Streamlit is an open-source Python framework for building data apps and web interfaces
- **Why**: Provides rapid development of interactive web UIs with minimal code
- **Role**: Handles the entire user interface, chat display, and user interactions

### **Backend: FastAPI**
- **What**: FastAPI is a modern, high-performance web framework for building APIs with Python
- **Why**: Offers async support, automatic API documentation, and excellent performance
- **Role**: Acts as middleware between the frontend and Ollama, handling API requests

### **LLM Runtime: Ollama**
- **What**: Ollama is a tool for running large language models locally
- **Why**: Enables running powerful AI models on your own hardware without cloud dependencies
- **Role**: Executes the actual LLM inference and generates responses

### **Additional Libraries**
- **requests**: HTTP library for making API calls between components
- **json**: For storing and managing chat history
- **datetime**: For timestamping messages and organizing chats

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Ollama**
   - Download from: [https://ollama.ai](https://ollama.ai)
   - Install and verify:
     ```bash
     ollama --version
     ```

3. **At least one Ollama model**
   ```bash
   ollama pull llama3
   ```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd "Chat App"
```

### 2. Create a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install streamlit fastapi uvicorn requests
```

Or create a `requirements.txt` file:
```txt
streamlit>=1.28.0
fastapi>=0.104.0
uvicorn>=0.24.0
requests>=2.31.0
```

Then install:
```bash
pip install -r requirements.txt
```

## 🎯 How to Run

### Step 1: Start Ollama Service
Ensure Ollama is running in the background:
```bash
ollama serve
```

### Step 2: Start the FastAPI Backend
Open a terminal and run:
```bash
uvicorn api:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Step 3: Start the Streamlit Frontend
Open another terminal and run:
```bash
streamlit run chat_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Chat App/
│
├── chat_app.py           # Streamlit frontend application
├── api.py                # FastAPI backend server
├── chat_history.json     # Persistent chat storage (auto-generated)
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
└── requirements.txt      # Python dependencies (optional)
```

## 🔧 Configuration

### Available Models
The application supports the following Ollama models by default:
- `llama3` - Meta's Llama 3 model
- `llama2` - Meta's Llama 2 model
- `mistral` - Mistral AI's model
- `codellama` - Code-specialized Llama model
- `phi` - Microsoft's Phi model
- `neural-chat` - Intel's Neural Chat model

To add more models:
1. Pull the model with Ollama: `ollama pull <model-name>`
2. Add it to the `model_options` list in `chat_app.py`

### API Configuration
- **Backend Port**: Default is `8000` (configurable in `api.py`)
- **Frontend Port**: Default is `8501` (Streamlit default)
- **Ollama URL**: Default is `http://localhost:11434`

## 💡 Usage

1. **Start a New Chat**: Click the "➕ New Chat" button in the sidebar
2. **Select a Model**: Choose your preferred LLM from the dropdown
3. **Send Messages**: Type your message in the input box and press Enter
4. **View History**: Click on any previous chat in the sidebar to load it
5. **Delete Chats**: Click the 🗑️ icon next to any chat to remove it
6. **Clear All**: Use "Clear All History" to remove all saved conversations

## 🎨 UI Features

- **Welcome Screen**: Example prompts to get started quickly
- **Message Timestamps**: Track when each message was sent
- **Connection Status**: Visual indicator showing API connectivity
- **Compact Design**: Minimalist interface maximizing chat space
- **Persistent Storage**: All chats automatically saved to `chat_history.json`

## 🐛 Troubleshooting

### API Connection Error
**Problem**: "Cannot connect to API" message appears

**Solutions**:
1. Ensure FastAPI is running: `uvicorn api:app --reload --port 8000`
2. Check if port 8000 is available
3. Verify the API_URL in `chat_app.py` matches your backend

### Ollama Connection Error
**Problem**: Requests timeout or fail

**Solutions**:
1. Ensure Ollama is running: `ollama serve`
2. Verify Ollama is on port 11434: `curl http://localhost:11434`
3. Check if the selected model is downloaded: `ollama list`

### Model Not Found
**Problem**: Error when sending messages

**Solution**: Download the model first:
```bash
ollama pull llama3
```

## 🔐 Privacy & Security

- ✅ All data processing happens locally
- ✅ No external API calls or data transmission
- ✅ Chat history stored locally in `chat_history.json`
- ✅ Complete control over your data and models

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Streamlit** - For the amazing UI framework
- **FastAPI** - For the high-performance backend framework
- **Ollama** - For making local LLMs accessible
- **Meta, Mistral AI, Microsoft** - For open-source LLM models

## 📧 Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section
2. Review Ollama documentation: [https://ollama.ai/docs](https://ollama.ai/docs)
3. Check Streamlit docs: [https://docs.streamlit.io](https://docs.streamlit.io)

---

**Made with ❤️ for privacy-conscious AI enthusiasts**
