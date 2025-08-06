import streamlit as st
import requests
import json
import time
from datetime import datetime
import re
from typing import List, Dict, Any, Optional
import base64
import io

# Page config
st.set_page_config(
    page_title="Ollama Chat Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = []
if 'system_prompt' not in st.session_state:
    st.session_state.system_prompt = "You are a helpful assistant."
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7
if 'top_p' not in st.session_state:
    st.session_state.top_p = 0.9
if 'max_tokens' not in st.session_state:
    st.session_state.max_tokens = 2048
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'show_thinking' not in st.session_state:
    st.session_state.show_thinking = {}

# Custom CSS for theming and styling
def apply_custom_css():
    theme_colors = {
        'dark': {
            'bg': '#1a1a1a',
            'card': '#2d2d2d',
            'text': '#ffffff',
            'border': '#404040',
            'thinking': '#3a3a4a',
            'accent': '#4CAF50'
        },
        'light': {
            'bg': '#ffffff',
            'card': '#f5f5f5',
            'text': '#333333',
            'border': '#dddddd',
            'thinking': '#f0f0f5',
            'accent': '#4CAF50'
        }
    }
    
    colors = theme_colors[st.session_state.theme]
    
    # Light mode specific overrides
    light_mode_css = ""
    if st.session_state.theme == 'light':
        light_mode_css = f"""
        /* Core Streamlit component overrides for light mode */
        .stApp > header {{
            background-color: transparent !important;
        }}
        
        .stApp .main .block-container {{
            background-color: {colors['bg']} !important;
            color: {colors['text']} !important;
        }}
        
        /* Sidebar styling */
        .stSidebar .stSidebar-content {{
            background-color: {colors['card']} !important;
            border-right: 1px solid {colors['border']} !important;
        }}
        
        .stSidebar .stSidebar-content * {{
            color: {colors['text']} !important;
        }}
        
        /* Text elements */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
            color: {colors['text']} !important;
        }}
        
        .stApp p, .stApp div, .stApp span, .stApp li {{
            color: {colors['text']} !important;
        }}
        
        .stApp .stMarkdown {{
            color: {colors['text']} !important;
        }}
        
        /* Input elements */
        .stTextInput input, .stTextArea textarea, .stNumberInput input {{
            background-color: {colors['bg']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {{
            border-color: {colors['accent']} !important;
            box-shadow: 0 0 0 1px {colors['accent']} !important;
        }}
        
        /* Chat input */
        .stChatInput input {{
            background-color: {colors['bg']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        .stChatInput input:focus {{
            border-color: {colors['accent']} !important;
            box-shadow: 0 0 0 1px {colors['accent']} !important;
        }}
        
        /* Buttons */
        .stButton button {{
            background-color: {colors['card']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        .stButton button:hover {{
            background-color: {colors['thinking']} !important;
            border-color: {colors['accent']} !important;
        }}
        
        .stButton button:active, .stButton button:focus {{
            background-color: {colors['accent']} !important;
            color: white !important;
            border-color: {colors['accent']} !important;
        }}
        
        /* Select boxes and dropdowns */
        .stSelectbox select, .stMultiSelect select {{
            background-color: {colors['bg']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        .stSelectbox select:focus, .stMultiSelect select:focus {{
            border-color: {colors['accent']} !important;
            box-shadow: 0 0 0 1px {colors['accent']} !important;
        }}
        
        /* Multiselect */
        .stMultiSelect .multiselect-container {{
            background-color: {colors['bg']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        .stMultiSelect .multiselect-container .multiselect-tag {{
            background-color: {colors['thinking']} !important;
            color: {colors['text']} !important;
        }}
        
        /* Sliders */
        .stSlider .slider-container {{
            color: {colors['text']} !important;
        }}
        
        .stSlider .slider-track {{
            background-color: {colors['border']} !important;
        }}
        
        .stSlider .slider-thumb {{
            background-color: {colors['accent']} !important;
        }}
        
        /* Checkboxes */
        .stCheckbox label {{
            color: {colors['text']} !important;
        }}
        
        .stCheckbox input:checked + span {{
            background-color: {colors['accent']} !important;
        }}
        
        /* Expanders */
        .stExpander {{
            border: 1px solid {colors['border']} !important;
            background-color: {colors['card']} !important;
        }}
        
        .stExpander .streamlit-expanderHeader {{
            background-color: {colors['card']} !important;
            color: {colors['text']} !important;
        }}
        
        .stExpander .streamlit-expanderContent {{
            background-color: {colors['bg']} !important;
            color: {colors['text']} !important;
        }}
        
        /* Columns */
        .stColumns .stColumn {{
            background-color: transparent !important;
        }}
        
        /* Chat messages */
        .stChatMessage {{
            background-color: {colors['card']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        .stChatMessage .stChatMessage-content {{
            color: {colors['text']} !important;
        }}
        
        .stChatMessage .stChatMessage-avatar {{
            background-color: {colors['thinking']} !important;
        }}
        
        /* Captions and labels */
        .stApp .stCaption {{
            color: {colors['text']} !important;
            opacity: 0.7 !important;
        }}
        
        /* Download button */
        .stDownloadButton button {{
            background-color: {colors['accent']} !important;
            color: white !important;
            border: none !important;
        }}
        
        .stDownloadButton button:hover {{
            background-color: #45a049 !important;
        }}
        
        /* Code blocks */
        .stApp pre, .stApp code {{
            background-color: {colors['thinking']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        /* Tables */
        .stDataFrame, .stTable {{
            background-color: {colors['bg']} !important;
            color: {colors['text']} !important;
        }}
        
        /* Metric widgets */
        .stMetric {{
            background-color: {colors['card']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        .stMetric .metric-label {{
            color: {colors['text']} !important;
        }}
        
        .stMetric .metric-value {{
            color: {colors['text']} !important;
        }}
        
        /* Progress bars */
        .stProgress .progress-bar {{
            background-color: {colors['accent']} !important;
        }}
        
        /* Alerts */
        .stAlert {{
            background-color: {colors['card']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border']} !important;
        }}
        
        /* Success/Error/Warning messages */
        .stSuccess, .stError, .stWarning, .stInfo {{
            color: {colors['text']} !important;
        }}
        
        /* Sidebar specific styling improvements */
        .stSidebar .stTitle {{
            color: {colors['text']} !important;
            font-weight: 600 !important;
            text-shadow: none !important;
        }}
        
        .stSidebar .stSubheader {{
            color: {colors['text']} !important;
            font-weight: 500 !important;
            margin-top: 1.5rem !important;
            margin-bottom: 0.5rem !important;
            text-shadow: none !important;
        }}
        
        /* Enhanced sidebar typography */
        .stSidebar h1, .stSidebar h2, .stSidebar h3 {{
            color: {colors['text']} !important;
            font-weight: 600 !important;
            text-shadow: none !important;
        }}
        
        .stSidebar h1 {{
            font-size: 1.5rem !important;
            border-bottom: 2px solid {colors['accent']} !important;
            padding-bottom: 0.5rem !important;
            margin-bottom: 1rem !important;
        }}
        
        .stSidebar h2 {{
            font-size: 1.2rem !important;
            color: #2c3e50 !important;
            margin-top: 1.5rem !important;
        }}
        
        /* Label improvements */
        .stSidebar label {{
            color: {colors['text']} !important;
            font-weight: 500 !important;
        }}
        
        /* Enhanced sidebar background with subtle gradient */
        .stSidebar .stSidebar-content {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
            border-right: 2px solid {colors['border']} !important;
        }}
        
        /* Improved section dividers */
        .stSidebar hr {{
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, {colors['border']}, transparent) !important;
            margin: 1.5rem 0 !important;
        }}
        
        /* Enhanced widget containers */
        .stSidebar > div > div > div {{
            background-color: rgba(255, 255, 255, 0.7) !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
            margin-bottom: 1rem !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
        }}
        
        /* Checkbox styling improvements */
        .stSidebar .stCheckbox > label > div:first-child {{
            background-color: {colors['bg']} !important;
            border: 2px solid {colors['border']} !important;
        }}
        
        .stSidebar .stCheckbox > label > div:first-child[aria-checked="true"] {{
            background-color: {colors['accent']} !important;
            border-color: {colors['accent']} !important;
        }}
        
        /* Enhanced number input styling */
        .stSidebar .stNumberInput > label {{
            color: {colors['text']} !important;
            font-weight: 500 !important;
        }}
        
        /* Text area label styling */
        .stSidebar .stTextArea > label {{
            color: {colors['text']} !important;
            font-weight: 500 !important;
        }}
        
        /* Expander header improvements in sidebar */
        .stSidebar .streamlit-expanderHeader {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            color: {colors['text']} !important;
            font-weight: 500 !important;
            border: 1px solid {colors['border']} !important;
            border-radius: 6px !important;
        }}
        
        .stSidebar .streamlit-expanderHeader:hover {{
            background-color: {colors['accent']} !important;
            color: white !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        }}
        
        /* Download button enhancements */
        .stSidebar .stDownloadButton button {{
            background: linear-gradient(135deg, {colors['accent']}, #45a049) !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }}
        
        .stSidebar .stDownloadButton button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3) !important;
        }}
        
        /* Main content title styling */
        .main h1 {{
            color: {colors['text']} !important;
            font-weight: 600 !important;
            border-bottom: 2px solid {colors['accent']} !important;
            padding-bottom: 0.5rem !important;
            margin-bottom: 1.5rem !important;
        }}
        
        /* Enhanced visual hierarchy for captions */
        .stApp .stCaption {{
            color: #6c757d !important;
            font-size: 0.875rem !important;
            font-weight: 400 !important;
        }}
        """
    
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {colors['bg']};
            color: {colors['text']};
        }}
        
        {light_mode_css}
        
        .chat-message {{
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin-bottom: 1rem;
            background-color: {colors['card']};
            border: 1px solid {colors['border']};
            color: {colors['text']};
            animation: slideIn 0.3s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .thinking-section {{
            background-color: {colors['thinking']};
            border-left: 3px solid {colors['accent']};
            padding: 0.8rem;
            margin-top: 0.5rem;
            border-radius: 0.5rem;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            opacity: 0.9;
            color: {colors['text']};
        }}
        
        .model-header {{
            font-weight: bold;
            color: {colors['accent']};
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .token-stats {{
            display: inline-block;
            padding: 0.3rem 0.6rem;
            background-color: {colors['thinking']};
            border-radius: 0.4rem;
            font-size: 0.85em;
            margin-left: 0.5rem;
            color: {colors['text']};
        }}
        
        .comparison-column {{
            padding: 1rem;
            border-right: 1px solid {colors['border']};
        }}
        
        .copy-button {{
            cursor: pointer;
            padding: 0.2rem 0.5rem;
            border-radius: 0.3rem;
            background-color: {colors['thinking']};
            transition: all 0.2s;
            color: {colors['text']};
        }}
        
        .copy-button:hover {{
            background-color: {colors['accent']};
            color: white;
            transform: scale(1.05);
        }}
        
        /* Enhanced visual polish for light mode */
        .thinking-section {{
            background: linear-gradient(135deg, {colors['thinking']}, #f8f9ff) !important;
            border-left: 3px solid {colors['accent']} !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
            color: {colors['text']} !important;
        }}
        
        .token-stats {{
            background: linear-gradient(135deg, {colors['thinking']}, #f0f0f8) !important;
            color: {colors['text']} !important;
            border: 1px solid rgba(76, 175, 80, 0.2) !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        }}
        
        .model-header {{
            color: {colors['accent']} !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
        }}
        
        /* Enhanced main content styling */
        .main .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            background-color: {colors['bg']} !important;
        }}
        
        /* Light mode chat message enhancements */
        .stChatMessage {{
            background: linear-gradient(135deg, {colors['card']}, #f8f9fa) !important;
            border: 1px solid {colors['border']} !important;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.2s ease !important;
        }}
        
        .stChatMessage:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
            transform: translateY(-1px) !important;
        }}
        
        /* Enhanced button styling for light mode */
        .stButton button {{
            background: linear-gradient(135deg, {colors['card']}, #f0f0f0) !important;
            border: 1px solid {colors['border']} !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.2s ease !important;
        }}
        
        .stButton button:hover {{
            background: linear-gradient(135deg, {colors['accent']}, #45a049) !important;
            color: white !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.25) !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# Ollama API functions
def get_available_models():
    """Fetch available models from Ollama"""
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [model['name'] for model in models]
        return []
    except:
        return []

def extract_thinking_tokens(text):
    """Extract thinking tokens from response (for models like deepseek-r1)"""
    thinking_pattern = r'<think>(.*?)</think>'
    thinking_matches = re.findall(thinking_pattern, text, re.DOTALL)
    
    # Remove thinking tokens from main response
    clean_text = re.sub(thinking_pattern, '', text, flags=re.DOTALL).strip()
    
    # Also check for other thinking patterns
    if not thinking_matches:
        # Check for <thinking> tags
        thinking_pattern2 = r'<thinking>(.*?)</thinking>'
        thinking_matches = re.findall(thinking_pattern2, text, re.DOTALL)
        clean_text = re.sub(thinking_pattern2, '', text, flags=re.DOTALL).strip()
    
    return clean_text, ' '.join(thinking_matches) if thinking_matches else None

def stream_ollama_response(model, messages, temperature, top_p, max_tokens):
    """Stream response from Ollama API"""
    url = 'http://localhost:11434/api/chat'
    
    payload = {
        'model': model,
        'messages': messages,
        'stream': True,
        'options': {
            'temperature': temperature,
            'top_p': top_p,
            'num_predict': max_tokens
        }
    }
    
    try:
        response = requests.post(url, json=payload, stream=True)
        
        full_response = ""
        tokens = 0
        start_time = time.time()
        
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                if 'message' in json_response:
                    content = json_response['message'].get('content', '')
                    full_response += content
                    tokens += 1
                    yield content, tokens, time.time() - start_time
                    
                if json_response.get('done', False):
                    # Get final statistics
                    eval_count = json_response.get('eval_count', tokens)
                    eval_duration = json_response.get('eval_duration', 0) / 1e9  # Convert to seconds
                    tokens_per_sec = eval_count / eval_duration if eval_duration > 0 else 0
                    yield None, eval_count, tokens_per_sec
                    
    except Exception as e:
        yield f"Error: {str(e)}", 0, 0

def copy_to_clipboard(text):
    """Create a copy button with JavaScript"""
    return f"""
    <script>
    function copyToClipboard(text) {{
        navigator.clipboard.writeText(text);
    }}
    </script>
    """

def export_conversation(format='json'):
    """Export conversation history"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format == 'json':
        content = json.dumps(st.session_state.messages, indent=2)
        mime = 'application/json'
        ext = 'json'
    elif format == 'markdown':
        content = "# Conversation History\n\n"
        for msg in st.session_state.messages:
            role = msg['role'].capitalize()
            content += f"## {role}\n{msg['content']}\n\n"
        mime = 'text/markdown'
        ext = 'md'
    else:  # txt
        content = ""
        for msg in st.session_state.messages:
            role = msg['role'].upper()
            content += f"{role}: {msg['content']}\n\n"
        mime = 'text/plain'
        ext = 'txt'
    
    return content, f"conversation_{timestamp}.{ext}", mime

# Main UI
apply_custom_css()

# Sidebar
with st.sidebar:
    st.title("🤖 Ollama Chat Studio")
    
    # Theme toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light"):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
    
    # Model selection
    st.subheader("Model Selection")
    available_models = get_available_models()
    
    if not available_models:
        st.error("No Ollama models found. Make sure Ollama is running.")
    else:
        comparison_mode = st.checkbox("Compare Models", value=st.session_state.comparison_mode)
        st.session_state.comparison_mode = comparison_mode
        
        if comparison_mode:
            selected_models = st.multiselect(
                "Select models to compare:",
                available_models,
                default=st.session_state.selected_models[:len(available_models)] if st.session_state.selected_models else []
            )
            st.session_state.selected_models = selected_models
        else:
            selected_model = st.selectbox("Select model:", available_models)
            st.session_state.selected_models = [selected_model]
    
    # Model parameters
    with st.expander("⚙️ Model Parameters", expanded=False):
        st.session_state.temperature = st.slider(
            "Temperature", 0.0, 2.0, st.session_state.temperature, 0.1
        )
        st.session_state.top_p = st.slider(
            "Top P", 0.0, 1.0, st.session_state.top_p, 0.1
        )
        st.session_state.max_tokens = st.number_input(
            "Max Tokens", 1, 8192, st.session_state.max_tokens
        )
    
    # System prompt
    with st.expander("📝 System Prompt", expanded=False):
        st.session_state.system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.system_prompt,
            height=100
        )
    
    # Chat controls
    st.subheader("Chat Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.show_thinking = {}
            st.rerun()
    
    with col2:
        if st.button("🔄 Regenerate"):
            if st.session_state.messages and st.session_state.messages[-1]['role'] == 'assistant':
                st.session_state.messages.pop()
                st.rerun()
    
    # Export options
    with st.expander("💾 Export Conversation", expanded=False):
        export_format = st.selectbox("Format:", ['json', 'markdown', 'txt'])
        if st.button("Export"):
            content, filename, mime = export_conversation(export_format)
            st.download_button(
                label="Download",
                data=content,
                file_name=filename,
                mime=mime
            )

# Main chat area
st.title("Chat Interface")

# Display token count for input
if st.session_state.messages:
    last_user_msg = next((msg for msg in reversed(st.session_state.messages) if msg['role'] == 'user'), None)
    if last_user_msg:
        token_estimate = len(last_user_msg['content'].split()) * 1.3  # Rough estimate
        st.caption(f"Last input: ~{int(token_estimate)} tokens")

# Chat history display
if st.session_state.comparison_mode and len(st.session_state.selected_models) > 1:
    # Display in columns for comparison
    cols = st.columns(len(st.session_state.selected_models))
    
    for idx, model in enumerate(st.session_state.selected_models):
        with cols[idx]:
            st.markdown(f"### {model}")
            
            for msg in st.session_state.messages:
                if msg['role'] == 'user':
                    st.markdown(f"**You:** {msg['content']}")
                elif msg['role'] == 'assistant' and msg.get('model') == model:
                    # Display response with thinking tokens handling
                    response_data = msg.get('response_data', {})
                    clean_content = response_data.get('clean_content', msg['content'])
                    thinking = response_data.get('thinking', None)
                    stats = response_data.get('stats', {})
                    
                    st.markdown(f"**{model}:**")
                    st.markdown(clean_content)
                    
                    # Show stats
                    if stats:
                        st.caption(f"📊 {stats.get('tokens', 0)} tokens | {stats.get('tokens_per_sec', 0):.1f} tok/s")
                    
                    # Thinking tokens in expander
                    if thinking:
                        with st.expander("🤔 Thinking Process", expanded=False):
                            st.markdown(f"```\n{thinking}\n```")
else:
    # Single model display
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            with st.chat_message("user"):
                st.markdown(msg['content'])
        elif msg['role'] == 'assistant':
            with st.chat_message("assistant"):
                response_data = msg.get('response_data', {})
                clean_content = response_data.get('clean_content', msg['content'])
                thinking = response_data.get('thinking', None)
                stats = response_data.get('stats', {})
                
                st.markdown(clean_content)
                
                # Show stats
                if stats:
                    st.caption(f"📊 {stats.get('tokens', 0)} tokens | {stats.get('tokens_per_sec', 0):.1f} tok/s")
                
                # Thinking tokens in expander
                if thinking:
                    with st.expander("🤔 Thinking Process", expanded=False):
                        st.markdown(f"```\n{thinking}\n```")

# Chat input
user_input = st.chat_input("Type your message...")

if user_input and st.session_state.selected_models:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Prepare messages for API
    api_messages = [{"role": "system", "content": st.session_state.system_prompt}]
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            api_messages.append({"role": "user", "content": msg['content']})
        elif msg['role'] == 'assistant' and not msg.get('model'):
            # Include previous responses for context
            api_messages.append({"role": "assistant", "content": msg['content']})
    
    # Generate responses
    if st.session_state.comparison_mode and len(st.session_state.selected_models) > 1:
        # Multiple model responses
        response_cols = st.columns(len(st.session_state.selected_models))
        
        for idx, model in enumerate(st.session_state.selected_models):
            with response_cols[idx]:
                st.markdown(f"**{model}:**")
                response_placeholder = st.empty()
                
                full_response = ""
                final_stats = {}
                
                for chunk, tokens, time_or_tps in stream_ollama_response(
                    model, api_messages, 
                    st.session_state.temperature,
                    st.session_state.top_p,
                    st.session_state.max_tokens
                ):
                    if chunk is not None:
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    else:
                        final_stats = {'tokens': tokens, 'tokens_per_sec': time_or_tps}
                
                # Process thinking tokens
                clean_content, thinking = extract_thinking_tokens(full_response)
                response_placeholder.markdown(clean_content)
                
                # Store in session state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": clean_content,
                    "model": model,
                    "response_data": {
                        "clean_content": clean_content,
                        "thinking": thinking,
                        "stats": final_stats
                    }
                })
                
                # Display stats
                if final_stats:
                    st.caption(f"📊 {final_stats['tokens']} tokens | {final_stats['tokens_per_sec']:.1f} tok/s")
                
                # Display thinking if present
                if thinking:
                    with st.expander("🤔 Thinking Process", expanded=False):
                        st.markdown(f"```\n{thinking}\n```")
    else:
        # Single model response
        model = st.session_state.selected_models[0]
        
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            full_response = ""
            final_stats = {}
            
            for chunk, tokens, time_or_tps in stream_ollama_response(
                model, api_messages,
                st.session_state.temperature,
                st.session_state.top_p,
                st.session_state.max_tokens
            ):
                if chunk is not None:
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                else:
                    final_stats = {'tokens': tokens, 'tokens_per_sec': time_or_tps}
            
            # Process thinking tokens
            clean_content, thinking = extract_thinking_tokens(full_response)
            response_placeholder.markdown(clean_content)
            
            # Store in session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": clean_content,
                "response_data": {
                    "clean_content": clean_content,
                    "thinking": thinking,
                    "stats": final_stats
                }
            })
            
            # Display stats
            if final_stats:
                st.caption(f"📊 {final_stats['tokens']} tokens | {final_stats['tokens_per_sec']:.1f} tok/s")
            
            # Display thinking if present
            if thinking:
                with st.expander("🤔 Thinking Process", expanded=False):
                    st.markdown(f"```\n{thinking}\n```")
    
    st.rerun()

# Footer
st.markdown("---")
st.caption("🚀 Powered by Ollama | Made with Streamlit | © Brian Laughlin | MIT License")
