import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# Page Configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Remove white backgrounds */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove white blocks and borders */
    .block-container {
        padding-top: 2rem;
        background: transparent;
    }
    
    .element-container {
        background: transparent;
    }
    
    div[data-testid="stVerticalBlock"] {
        background: transparent;
        border: none;
    }
    
    div[data-testid="stHorizontalBlock"] {
        background: transparent;
        border: none;
    }
    
    div[data-testid="column"] {
        background: transparent;
        border: none;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        border: none;
    }
    
    /* Custom scrollbar */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.05);
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Message bubbles with smooth animations */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        animation: slideInRight 0.3s ease-out;
        transition: all 0.3s ease;
        border: none;
    }
    
    .user-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    .ai-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        animation: slideInLeft 0.3s ease-out;
        transition: all 0.3s ease;
        border: none;
    }
    
    .ai-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.5);
    }
    
    /* Animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 2rem 0;
        color: white;
        animation: fadeIn 0.6s ease-out;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Input styling - FIXED text visibility and borders */
    .stTextInput {
        border: none !important;
    }
    
    .stTextInput > div {
        border: none !important;
        background: transparent !important;
    }
    
    .stTextInput > div > div {
        border: none !important;
        background: transparent !important;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        padding: 1rem 1.5rem !important;
        font-size: 1rem !important;
        background: rgba(255, 255, 255, 0.95) !important;
        transition: all 0.3s ease !important;
        outline: none !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        color: #333 !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(0, 0, 0, 0.4) !important;
        font-weight: 400 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid #667eea !important;
        outline: none !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3) !important;
        transform: translateY(-2px);
        background: white !important;
    }
    
    /* Remove default focus outline */
    input:focus-visible {
        outline: none !important;
    }
    
    /* Button styling with smooth transitions */
    .stButton {
        border: none !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:focus {
        outline: none !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* History section */
    .history-title {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(255,255,255,0.3);
    }
    
    /* Info and metric boxes */
    .stMetric {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        border: none !important;
    }
    
    .stMetric:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: scale(1.02);
    }
    
    .stAlert {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        border: none !important;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Spinner animation */
    .stSpinner > div {
        border-color: white !important;
        border-right-color: transparent !important;
    }
    
    /* Sidebar metric styling */
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Remove white dividers and borders */
    hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
        border-style: solid !important;
        border-width: 1px 0 0 0 !important;
        margin: 2rem 0 !important;
    }
    
    /* Remove all unwanted borders globally */
    * {
        border-color: transparent;
    }
    
    /* Info box text color */
    .stAlert p {
        color: #333 !important;
    }
    
    /* Warning box */
    .stWarning {
        background: rgba(255, 193, 7, 0.95) !important;
        border: none !important;
        border-radius: 15px !important;
    }
    
    .stWarning p {
        color: #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load AI Model
@st.cache_resource
def load_model():
    return OllamaLLM(model="llama3.2:1b")

llm = load_model()

# Initialize Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

# Initialize input clear flag
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Define AI Chat Prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=(
        "You are a helpful AI assistant.\n"
        "Conversation so far:\n{chat_history}\n\n"
        "User: {question}\n"
        "Assistant:"
    )
)

# Function to run AI chat with memory
def run_chain(question):
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages]
    )
    
    with st.spinner("🤔 Thinking..."):
        response = llm.invoke(
            prompt.format(chat_history=chat_history_text, question=question)
        )
    
    # Store conversation in memory
    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)
    
    return response

# Header
st.markdown("""
    <div class="header-container">
        <div class="header-title">🤖 AI Assistant</div>
        <div class="header-subtitle">Powered by Advanced Language Models</div>
    </div>
""", unsafe_allow_html=True)

# Main Chat Interface
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat Messages Display
    if st.session_state.chat_history.messages:
        for msg in st.session_state.chat_history.messages:
            if msg.type == "human":
                st.markdown(f'<div class="user-message">👤 {msg.content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-message">🤖 {msg.content}</div>', unsafe_allow_html=True)
    else:
        st.info("💬 Start a conversation by typing your question below!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input Section
    st.markdown("---")
    
    # Clear input after submission
    input_value = "" if st.session_state.clear_input else st.session_state.get("last_input", "")
    user_input = st.text_input("", placeholder="Type your message here...", label_visibility="collapsed", key="user_input", value=input_value)
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
    with col_btn2:
        send_button = st.button("Send 📤", use_container_width=True)
    
    if send_button and user_input:
        st.session_state.last_input = user_input
        response = run_chain(user_input)
        st.session_state.clear_input = True
        st.rerun()
    elif send_button and not user_input:
        st.warning("⚠️ Please enter a message first!")
    
    # Reset clear flag after rerun
    if st.session_state.clear_input:
        st.session_state.clear_input = False

# Sidebar with additional features
with st.sidebar:
    st.markdown('<div class="history-title">⚙️ Controls</div>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = ChatMessageHistory()
        st.session_state.clear_input = False
        st.rerun()
    
    st.markdown('<div class="history-title">📊 Statistics</div>', unsafe_allow_html=True)
    msg_count = len(st.session_state.chat_history.messages)
    st.metric("Total Messages", msg_count)
    st.metric("User Messages", msg_count // 2 if msg_count > 0 else 0)
    st.metric("AI Responses", msg_count // 2 if msg_count > 0 else 0)
    
    st.markdown('<div class="history-title">ℹ️ About</div>', unsafe_allow_html=True)
    st.info("""
        This AI assistant uses LangChain and Ollama to provide 
        intelligent responses with conversation memory.
        
        **Features:**
        - 💾 Persistent memory
        - 🎨 Beautiful UI
        - ⚡ Fast responses
        - 🔒 Local processing
    """)