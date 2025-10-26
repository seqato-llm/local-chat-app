import streamlit as st
import requests
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="Local LLM Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - ChatGPT-inspired clean design
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container */
    .main {
        background-color: #ffffff;
    }
    
    /* Sidebar styling - ChatGPT style */
    [data-testid="stSidebar"] {
        background-color: #f7f7f8;
        padding-top: 1rem;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        padding: 0.5rem 0;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: transparent;
        padding: 1.5rem 1rem;
        border-radius: 0;
    }
    
    [data-testid="stChatMessageContent"] {
        max-width: 48rem;
        margin: 0 auto;
    }
    
    /* User message background */
    .stChatMessage[data-testid*="user"] {
        background-color: #f7f7f8;
    }
    
    /* Assistant message background */
    .stChatMessage[data-testid*="assistant"] {
        background-color: #ffffff;
    }
    
    /* Chat input container */
    .stChatInputContainer {
        border-top: 1px solid #e5e5e5;
        padding: 1rem 0;
        background-color: #ffffff;
    }
    
    /* Button styling - minimal and clean */
    .stButton button {
        border-radius: 6px;
        border: 1px solid #d1d5db;
        background-color: transparent;
        color: #374151;
        font-weight: 500;
        padding: 0.4rem 0.75rem;
        transition: all 0.2s;
        width: 100%;
        height: 2.25rem;
        font-size: 0.875rem;
    }
    
    .stButton button:hover {
        background-color: #f3f4f6;
        border-color: #9ca3af;
    }
    
    /* Primary button (New Chat) */
    .primary-button button {
        background-color: #10a37f !important;
        color: white !important;
        border: none !important;
        font-weight: 600;
        height: 2.5rem !important;
    }
    
    .primary-button button:hover {
        background-color: #0d8f6f !important;
    }
    
    /* Chat history item styling */
    .chat-history-item {
        padding: 0.75rem;
        margin: 0.25rem 0;
        border-radius: 6px;
        cursor: pointer;
        transition: background-color 0.2s;
        border: 1px solid transparent;
    }
    
    .chat-history-item:hover {
        background-color: #ececf1;
    }
    
    .chat-history-item.active {
        background-color: #ececf1;
        border-color: #d1d5db;
    }
    
    /* Model selector - compact vertical spacing */
    .stSelectbox {
        margin-bottom: 0;
        margin-top: 0;
    }
    
    .stSelectbox > div {
        padding-top: 0;
        padding-bottom: 0;
        margin-bottom: 0;
    }
    
    .stSelectbox label {
        font-size: 0.875rem;
        margin-bottom: 0.25rem;
        padding-bottom: 0;
    }
    
    /* Sidebar section compact spacing */
    .sidebar-section {
        padding: 0;
        margin: 0.25rem 0;
    }
    
    /* Clean header */
    .chat-header {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        max-width: 48rem;
        margin: 0 auto;
    }
    
    .chat-header h1 {
        font-size: 2rem;
        font-weight: 600;
        color: #202123;
        margin-bottom: 0.5rem;
    }
    
    .chat-header p {
        color: #6e6e80;
        font-size: 0.95rem;
    }
    
    /* Sidebar sections */
    .sidebar-section {
        padding: 0.5rem 0;
        margin: 0.5rem 0;
    }
    
    .sidebar-title {
        font-size: 0.75rem;
        font-weight: 600;
        color: #6e6e80;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.25rem;
    }
    
    /* Status indicator */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 6px;
    }
    
    .status-online {
        background-color: #10a37f;
    }
    
    .status-offline {
        background-color: #ef4444;
    }
    
    /* Minimal scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:8000/chat"
CHAT_HISTORY_FILE = "chat_history.json"

# Helper functions for chat history management
def load_chat_history():
    """Load chat history from file"""
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_chat_history(history):
    """Save chat history to file"""
    try:
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Failed to save chat history: {e}")

def create_chat_title(messages):
    """Generate a title for the chat based on first user message"""
    for msg in messages:
        if msg["role"] == "user":
            title = msg["content"][:50]
            return title + "..." if len(msg["content"]) > 50 else title
    return "New Chat"

def get_chat_preview(messages):
    """Get a preview of the last message in chat"""
    if messages:
        last_msg = messages[-1]
        preview = last_msg["content"][:60]
        return preview + "..." if len(last_msg["content"]) > 60 else preview
    return "Empty chat"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama3"

# Sidebar
with st.sidebar:
    # New Chat Button
    st.markdown('<div class="primary-button">', unsafe_allow_html=True)
    if st.button("➕ New Chat", use_container_width=True, key="new_chat_btn"):
        # Save current chat if it has messages
        if st.session_state.messages and st.session_state.current_chat_id is None:
            chat_data = {
                "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "title": create_chat_title(st.session_state.messages),
                "messages": st.session_state.messages,
                "model": st.session_state.selected_model,
                "created_at": datetime.now().isoformat()
            }
            st.session_state.chat_history.insert(0, chat_data)
            save_chat_history(st.session_state.chat_history)
        
        # Start new chat
        st.session_state.messages = []
        st.session_state.current_chat_id = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model Selection
    model_options = ["llama3", "llama2", "mistral", "codellama", "phi", "neural-chat"]
    selected_model = st.selectbox(
        "🤖 Model",
        model_options,
        index=model_options.index(st.session_state.selected_model),
        label_visibility="visible"
    )
    st.session_state.selected_model = selected_model
    
    st.markdown("---")
    
    # Chat History
    st.markdown('<div class="sidebar-title">CHAT HISTORY</div>', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        for idx, chat in enumerate(st.session_state.chat_history):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                chat_title = chat.get("title", "Untitled Chat")
                if st.button(
                    f"💬 {chat_title}",
                    key=f"chat_{idx}",
                    use_container_width=True,
                    help=get_chat_preview(chat.get("messages", []))
                ):
                    # Load selected chat
                    st.session_state.messages = chat.get("messages", [])
                    st.session_state.current_chat_id = chat.get("id")
                    st.session_state.selected_model = chat.get("model", "llama3")
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{idx}", help="Delete chat"):
                    st.session_state.chat_history.pop(idx)
                    save_chat_history(st.session_state.chat_history)
                    if st.session_state.current_chat_id == chat.get("id"):
                        st.session_state.messages = []
                        st.session_state.current_chat_id = None
                    st.rerun()
    else:
        st.markdown('<p style="text-align: center; color: #6e6e80; padding: 1rem; font-size: 0.9rem;">No chat history yet</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Clear All History
    if st.session_state.chat_history:
        if st.button("🗑️ Clear All History", use_container_width=True):
            st.session_state.chat_history = []
            save_chat_history(st.session_state.chat_history)
            st.session_state.messages = []
            st.session_state.current_chat_id = None
            st.rerun()
    
    st.markdown("---")
    
    # Connection Status
    try:
        test_response = requests.get("http://localhost:8000/", timeout=1)
        st.markdown('<div style="padding: 0.75rem; font-size: 0.9rem;"><span class="status-indicator status-online"></span>API Connected</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="padding: 0.75rem; font-size: 0.9rem;"><span class="status-indicator status-offline"></span>API Disconnected</div>', unsafe_allow_html=True)

# Main content area
if not st.session_state.messages:
    # Welcome screen
    st.markdown("""
    <div class="chat-header">
        <h1>💬 Local LLM Chat</h1>
        <p>Chat with AI models running locally on your machine</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Example prompts
    col1, col2, col3 = st.columns(3)
    
    example_prompts = [
        "Explain quantum computing",
        "Write a Python function",
        "Help me debug code"
    ]
    
    with col1:
        if st.button(f"💡 {example_prompts[0]}", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": example_prompts[0],
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    with col2:
        if st.button(f"💡 {example_prompts[1]}", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": example_prompts[1],
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    with col3:
        if st.button(f"💡 {example_prompts[2]}", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": example_prompts[2],
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Message Local LLM...", key="chat_input"):
    # Add user message
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner(""):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "prompt": prompt,
                        "model": st.session_state.selected_model
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    output = response.json()["response"]
                    message_placeholder.markdown(output)
                    
                    response_timestamp = datetime.now().strftime("%H:%M")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": output,
                        "timestamp": response_timestamp
                    })
                    
                    # Auto-save to history if this is a new chat with multiple messages
                    if st.session_state.current_chat_id is None and len(st.session_state.messages) >= 2:
                        chat_data = {
                            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                            "title": create_chat_title(st.session_state.messages),
                            "messages": st.session_state.messages.copy(),
                            "model": st.session_state.selected_model,
                            "created_at": datetime.now().isoformat()
                        }
                        st.session_state.chat_history.insert(0, chat_data)
                        st.session_state.current_chat_id = chat_data["id"]
                        save_chat_history(st.session_state.chat_history)
                    
                    # Update existing chat in history
                    elif st.session_state.current_chat_id is not None:
                        for chat in st.session_state.chat_history:
                            if chat.get("id") == st.session_state.current_chat_id:
                                chat["messages"] = st.session_state.messages.copy()
                                chat["title"] = create_chat_title(st.session_state.messages)
                                save_chat_history(st.session_state.chat_history)
                                break
                    
                else:
                    error_msg = f"⚠️ Error: API returned status code {response.status_code}"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                    
            except requests.exceptions.Timeout:
                error_msg = "⏱️ Request timed out. Please try again."
                message_placeholder.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
            except requests.exceptions.ConnectionError:
                error_msg = """🔌 Cannot connect to API. Please ensure:
                
1. FastAPI is running: `uvicorn api:app --reload --port 8000`
2. Ollama is running: `ollama serve`
3. Model is downloaded: `ollama pull """ + st.session_state.selected_model + "`"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
        
        st.rerun()
